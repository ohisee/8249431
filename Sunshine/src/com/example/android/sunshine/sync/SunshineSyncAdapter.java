/**
 *
 */
package com.example.android.sunshine.sync;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;
import java.util.Vector;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.accounts.Account;
import android.accounts.AccountManager;
import android.annotation.TargetApi;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.AbstractThreadedSyncAdapter;
import android.content.ContentProviderClient;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SyncRequest;
import android.content.SyncResult;
import android.database.Cursor;
import android.net.Uri;
import android.net.Uri.Builder;
import android.os.Build;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v4.app.NotificationCompat;
import android.support.v4.app.TaskStackBuilder;
import android.util.Log;

import com.example.android.sunshine.app.MainActivity;
import com.example.android.sunshine.app.R;
import com.example.android.sunshine.app.Utility;
import com.example.android.sunshine.app.data.WeatherContract;
import com.example.android.sunshine.app.data.WeatherContract.LocationEntry;
import com.example.android.sunshine.app.data.WeatherContract.WeatherEntry;

/**
 * Represents sunshine sync adapter.
 */
public class SunshineSyncAdapter extends AbstractThreadedSyncAdapter {

    // Interval at which to sync with the weather, in seconds.
    // 60 seconds (1 minute) * 180 = 3 hours
    public static final int SYNC_INTERVAL = 60 * 180;
    public static final int SYNC_FLEXTIME = SYNC_INTERVAL / 3;
    private static final String LOG_TAG = SunshineSyncAdapter.class.getSimpleName();
    private static final String[] NOTIFY_WEATHER_PROJECTION = new String[]{
            WeatherEntry.COLUMN_WEATHER_ID,
            WeatherEntry.COLUMN_MAX_TEMP,
            WeatherEntry.COLUMN_MIN_TEMP,
            WeatherEntry.COLUMN_SHORT_DESC};

    // these indices must match the projection
    private static final int INDEX_WEATHER_ID = 0;
    private static final int INDEX_MAX_TEMP = 1;
    private static final int INDEX_MIN_TEMP = 2;
    private static final int INDEX_SHORT_DESC = 3;

    // DAY_IN_MILLIS is the amount of milliseconds in a day
    private static final long DAY_IN_MILLIS = 1000 * 60 * 60 * 24;
    // WEATHER_NOTIFICATION_ID is an id you create that is matched to your notification so that you can reuse it
    private static final int WEATHER_NOTIFICATION_ID = 3004;

    public SunshineSyncAdapter(Context context, boolean autoInitialize) {
        super(context, autoInitialize);
    }

    /**
     * Helper method to have the sync adapter sync immediately
     *
     * @param Context context - The context used to access the account service
     */
    public static void syncImmediately(Context context) {
        Bundle bundle = new Bundle();
        bundle.putBoolean(ContentResolver.SYNC_EXTRAS_EXPEDITED, true);
        bundle.putBoolean(ContentResolver.SYNC_EXTRAS_MANUAL, true);
        ContentResolver.requestSync(getSyncAccount(context),
                context.getString(R.string.content_authority), bundle);
    }

    /**
     * Helper method to get the fake account to be used with SyncAdapter, or
     * make a new one if the fake account doesn't exist yet. If we make a new
     * account, we call the onAccountCreated method so we can initialize things.
     *
     * @param Context context - The context used to access the account service
     * @return a fake account.
     */
    public static Account getSyncAccount(Context context) {
        // Get an instance of the Android account manager
        AccountManager accountManager = (AccountManager) context
                .getSystemService(Context.ACCOUNT_SERVICE);

        // Create the account type and default account
        Account newAccount = new Account(context.getString(R.string.app_name),
                context.getString(R.string.sync_account_type));

        // If the password doesn't exist, the account doesn't exist
        if (null == accountManager.getPassword(newAccount)) {
            /*
			 * Add the account and account type, no password or user data If
			 * successful, return the Account object, otherwise report an error.
			 */
            if (!accountManager.addAccountExplicitly(newAccount, "", null)) {
                return null;
            }
			/*
			 * If you don't set android:syncable="true" in in your <provider>
			 * element in the manifest, then call
			 * ContentResolver.setIsSyncable(account, AUTHORITY, 1) here.
			 */
            onAccountCreated(newAccount, context);
        }
        return newAccount;
    }

    /**
     * Helper method to schedule the sync adapter periodic execution
     *
     * @param Context context
     * @param int     syncInterval
     * @param int     flexTime
     */
    @TargetApi(Build.VERSION_CODES.KITKAT)
    public static void configurePeriodicSync(Context context, int syncInterval, int flexTime) {
        Account account = getSyncAccount(context);
        String authority = context.getString(R.string.content_authority);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            SyncRequest request = new SyncRequest.Builder()
                    .syncPeriodic(syncInterval, flexTime)
                    .setSyncAdapter(account, authority).build();
            ContentResolver.requestSync(request);
        } else {
            ContentResolver.addPeriodicSync(account, authority, new Bundle(),
                    syncInterval);
        }
    }

    /**
     * On accounted (new) created, do configure periodic sync, set sync automatically, and trigger sync immediately.
     *
     * @param Account newAccount
     * @param Contex  context
     */
    private static void onAccountCreated(Account newAccount, Context context) {
		/*
		 * Since we've created an account
		 */
        SunshineSyncAdapter.configurePeriodicSync(context, SYNC_INTERVAL, SYNC_FLEXTIME);

		/*
		 * Without calling setSyncAutomatically, our periodic sync will not be
		 * enabled.
		 */
        ContentResolver.setSyncAutomatically(newAccount,
                context.getString(R.string.content_authority), true);

		/*
		 * Finally, let's do a sync to get things started
		 */
        syncImmediately(context);
    }

    /**
     * Initialize sync adapter. It is called in Main Activity's onCreate.
     *
     * @param Context context
     */
    public static void initializeSyncAdapter(Context context) {
        getSyncAccount(context);
    }

    @Override
    public void onPerformSync(Account account, Bundle extras, String authority,
                              ContentProviderClient provider, SyncResult syncResult) {

        Log.i(LOG_TAG, "SunshineSyncAdapter - onPerformSync");

        String locationQuery = Utility.getPreferredLocation(getContext());

        // If there's no zip code, there's nothing to look up. Verify size of params.
        if (null == locationQuery) {
            return;
        }

        // These two need to be declared outside the try/catch
        // so that they can be closed in the finally block.
        HttpURLConnection urlConnection = null;
        BufferedReader reader = null;
        // Will contain the raw JSON response as a string.
        String forecastJsonStr = null;

        String format = "json";
        String units = "metric";
        int daysCount = 14;
        //String locationQuery = inputs[0];// , units = inputs[1];

        try {
            //final String FORECAST_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast/daily?";
            // http://api.openweathermap.org/data/2.5/forecast/daily?q=94043&mode=json&units=metric&cnt=14
            final String QUERY_PARAM = "q";
            final String FORMAT_PARAM = "mode";
            final String UNITS_PARAM = "units";
            final String DAYS_PARAM = "cnt";

            // Build forecast data URL
            Builder uriBuilder = new Builder();
            uriBuilder
                    .scheme("http")
                    .authority("api.openweathermap.org")
                    .appendPath("data")
                    .appendPath("2.5")
                    .appendPath("forecast")
                    .appendPath("daily")
                    .appendQueryParameter(QUERY_PARAM, locationQuery)
                    .appendQueryParameter(FORMAT_PARAM, format)
                    .appendQueryParameter(UNITS_PARAM, units)
                    .appendQueryParameter(DAYS_PARAM,
                            Integer.toString(daysCount)).build();

            Log.i(LOG_TAG, uriBuilder.toString());

            // Construct the URL for the OpenWeatherMap query
            // Possible parameters are avaiable at OWM's forecast API page, at
            // http://openweathermap.org/API#forecast
            URL url = new URL(uriBuilder.toString());
            // Create the request to OpenWeatherMap, and open the connection
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod("GET");
            urlConnection.connect();
            // Read the input stream into a String
            InputStream inputStream = urlConnection.getInputStream();
            StringBuffer buffer = new StringBuffer();
            if (inputStream == null) {
                // Nothing to do.
                forecastJsonStr = null;
            }
            reader = new BufferedReader(new InputStreamReader(inputStream));
            String line;
            while ((line = reader.readLine()) != null) {
                // Since it's JSON, adding a newline isn't necessary (it
                // won't affect parsing)
                // But it does make debugging a *lot* easier if you print
                // out the completed
                // buffer for debugging.
                buffer.append(line + "\n");
            }

            if (buffer.length() == 0) {
                // Stream was empty. No point in parsing.
                forecastJsonStr = null;
            }
            forecastJsonStr = buffer.toString();
            // Log.i(LOG_TAG, forecastJsonStr);
        } catch (IOException e) {
            Log.e(LOG_TAG, "Error ", e);
            // If the code didn't successfully get the weather data, there's
            // no point in attemping to parse it.
            forecastJsonStr = null;
        } finally {
            if (urlConnection != null) {
                urlConnection.disconnect();
            }
            if (reader != null) {
                try {
                    reader.close();
                } catch (final IOException e) {
                    Log.e(LOG_TAG, "Error closing stream", e);
                }
            }
        }

        if (null != forecastJsonStr) {
            try {
                getWeatherDataFromJson(forecastJsonStr, daysCount, locationQuery);
            } catch (JSONException e) {
                Log.e(LOG_TAG, "Error getting weather data " + e.getMessage(), e);
            }
        }

        return;
    }

    /**
     * Take the String representing the complete forecast in JSON Format and
     * pull out the data we need to construct the Strings needed for the
     * wireframes.
     * <p>
     * Fortunately parsing is easy: constructor takes the JSON string and
     * converts it into an Object hierarchy for us.
     */
    private String[] getWeatherDataFromJson(String forecastJsonStr,
                                            int numDays, String locationSetting) throws JSONException {

        // These are the names of the JSON objects that need to be extracted.
        // Location information
        final String OWM_CITY = "city";
        final String OWM_CITY_NAME = "name";
        final String OWM_COORD = "coord";
        final String OWM_COORD_LAT = "lat";
        final String OWM_COORD_LONG = "lon";

        // Weather information. Each day's forecast info is an element of the
        // "list" array.
        final String OWM_LIST = "list";
        final String OWM_DATETIME = "dt";
        final String OWM_PRESSURE = "pressure";
        final String OWM_HUMIDITY = "humidity";
        final String OWM_WINDSPEED = "speed";
        final String OWM_WIND_DIRECTION = "deg";

        // All temperatures are children of the "temp" object.
        final String OWM_TEMPERATURE = "temp";
        final String OWM_MAX = "max";
        final String OWM_MIN = "min";
        final String OWM_WEATHER = "weather";
        final String OWM_DESCRIPTION = "main";
        final String OWM_WEATHER_ID = "id";

        JSONObject forecastJson = new JSONObject(forecastJsonStr);
        JSONArray weatherArray = forecastJson.getJSONArray(OWM_LIST);
        JSONObject cityJson = forecastJson.getJSONObject(OWM_CITY);
        String cityName = cityJson.getString(OWM_CITY_NAME);
        JSONObject coordJSON = cityJson.getJSONObject(OWM_COORD);
        double cityLatitude = coordJSON.getLong(OWM_COORD_LAT);
        double cityLongitude = coordJSON.getLong(OWM_COORD_LONG);

        Log.v(LOG_TAG, cityName + ", with coord: " + cityLatitude + " " + cityLongitude);
        // Insert the location into the database.
        // The function referenced here is not yet implemented, so we've
        // commented it out for now.
        long locationID = addLocation(locationSetting, cityName, cityLatitude, cityLongitude);

        // Get and insert the new weather information into the database
        Vector<ContentValues> cVector = new Vector<ContentValues>(weatherArray.length());

        String[] resultStrs = new String[numDays];
        for (int i = 0; i < weatherArray.length(); i++) {

            long dateTime;
            double pressure;
            int humidity;
            double windSpeed;
            double windDirection;

            double high;
            double low;

            int weatherId;

            // For now, using the format "Day, description, hi/low"
            String day;
            String description;
            String highAndLow;

            // Get the JSON object representing the day
            JSONObject dayForecast = weatherArray.getJSONObject(i);
            // The date/time is returned as a long. We need to convert that
            // into something human-readable, since most people won't read "1400356800" as "this saturday".
            dateTime = dayForecast.getLong(OWM_DATETIME);
            day = getReadableDateString(dateTime);
            humidity = dayForecast.getInt(OWM_HUMIDITY);
            pressure = dayForecast.getDouble(OWM_PRESSURE);
            windSpeed = dayForecast.getDouble(OWM_WINDSPEED);
            windDirection = dayForecast.getDouble(OWM_WIND_DIRECTION);

            // description is in a child array called "weather", which is 1 element long.
            JSONObject weatherObject = dayForecast.getJSONArray(OWM_WEATHER).getJSONObject(0);
            description = weatherObject.getString(OWM_DESCRIPTION);
            weatherId = weatherObject.getInt(OWM_WEATHER_ID);
            // Temperatures are in a child object called "temp". Try not to name variables
            // "temp" when working with temperature. It confuses everybody.
            JSONObject temperatureObject = dayForecast.getJSONObject(OWM_TEMPERATURE);

            high = temperatureObject.getDouble(OWM_MAX);
            low = temperatureObject.getDouble(OWM_MIN);

            ContentValues weatherValues = new ContentValues();

            weatherValues.put(WeatherEntry.COLUMN_LOC_KEY, locationID);
            weatherValues
                    .put(WeatherEntry.COLUMN_DATETEXT, WeatherContract
                            .getDbDateString(new Date(dateTime * 1000L)));
            weatherValues.put(WeatherEntry.COLUMN_HUMIDITY, humidity);
            weatherValues.put(WeatherEntry.COLUMN_PRESSURE, pressure);
            weatherValues.put(WeatherEntry.COLUMN_WIND_SPEED, windSpeed);
            weatherValues.put(WeatherEntry.COLUMN_DEGREES, windDirection);
            weatherValues.put(WeatherEntry.COLUMN_MAX_TEMP, high);
            weatherValues.put(WeatherEntry.COLUMN_MIN_TEMP, low);
            weatherValues.put(WeatherEntry.COLUMN_SHORT_DESC, description);
            weatherValues.put(WeatherEntry.COLUMN_WEATHER_ID, weatherId);

            cVector.add(weatherValues);

            highAndLow = formatHighLows(high, low);
            resultStrs[i] = day + " - " + description + " - " + highAndLow;
            Log.i(LOG_TAG, day + " - " + description + " - " + highAndLow +
                    " - " + weatherValues.getAsString(WeatherEntry.COLUMN_DATETEXT));
        }

        // Bulk insert weather data per location
        if (cVector.size() > 0) {

            getContext().getContentResolver().delete(WeatherEntry.CONTENT_URI, null, null);

            ContentValues[] values = cVector.toArray(new ContentValues[cVector.size()]);
            long rowsInserted = getContext().getContentResolver().bulkInsert(
                    WeatherEntry.CONTENT_URI, values);
            Log.v(LOG_TAG, "inserted " + rowsInserted + " rows of weather data");

            Calendar cal = Calendar.getInstance();
            cal.add(Calendar.DATE, -1); // Signifies yesterday's date
            String yesterdayDate = WeatherContract.getDbDateString(cal.getTime());
            getContext().getContentResolver().delete(WeatherEntry.CONTENT_URI,
                    WeatherEntry.COLUMN_DATETEXT + " <= ?",
                    new String[]{yesterdayDate});

            // Notification
            notifyWeather();
        }

        return resultStrs;
    }

    /**
     * The date/time conversion code is going to be moved outside the asynctask
     * later, so for convenience we're breaking it out into its own method now.
     */
    private String getReadableDateString(long time) {
        // Because the API returns a unix timestamp (measured in seconds),
        // it must be converted to milliseconds in order to be converted to
        // valid date.
        Date date = new Date(time * 1000);
        SimpleDateFormat format = new SimpleDateFormat("E, MMM d", Locale.getDefault());
        return format.format(date).toString();
    }

    /**
     * Prepare the weather high/lows for presentation.
     */
    private String formatHighLows(double high, double low) {
        // For presentation, assume the user doesn't care about tenths of a degree.

        Log.i(LOG_TAG, String.format("Before %s %s", high, low));

        SharedPreferences sharedPreferences = PreferenceManager
                .getDefaultSharedPreferences(getContext());

        String temperatureUnit = sharedPreferences.getString(
                getContext().getString(R.string.pref_temperature_unit_key),
                getContext().getString(R.string.pref_temperature_default_metric));

        Log.i(LOG_TAG, "--- Temperature Unit " + temperatureUnit);

        if (temperatureUnit
                .equalsIgnoreCase(getContext().getString(R.string.pref_temperature_imperial))) {
            high = ((high * 9) / 5) + 32;
            low = ((low * 9) / 5) + 32;
        } else if (!temperatureUnit
                .equalsIgnoreCase(getContext().getString(R.string.pref_temperature_default_metric))) {
            Log.d(LOG_TAG, "Unit not found + " + temperatureUnit);
        }

        long roundedHigh = Math.round(high);
        long roundedLow = Math.round(low);

        Log.i(LOG_TAG, String.format("After %s %s", roundedHigh, roundedLow));

        String highLowStr = roundedHigh + "/" + roundedLow;
        return highLowStr;
    }

    /**
     * Helper method to handle insertion of a new location in the weather
     * database.
     *
     * @param String locationSetting The location string used to request updates from the server.
     * @param String cityName A human-readable city name, e.g "Mountain View"
     * @param double lat the latitude of the city
     * @param double lon the longitude of the city
     * @return the row ID of the added location.
     */
    private long addLocation(String locationSetting, String cityName, double lat, double lon) {

        Log.i(LOG_TAG, String.format(
                "Inserting Location [%s], city name [%s], lat [%s], lon [%s]",
                locationSetting, cityName, lat, lon));

        Cursor cursor = getContext().getContentResolver().query(
                LocationEntry.CONTENT_URI,
                new String[]{WeatherContract.LocationEntry._ID},
                LocationEntry.COLUMN_LOCATION_SETTING + " = ?",
                new String[]{locationSetting}, null);

        long locationRowId;

        if (cursor.moveToFirst()) {
            Log.i(LOG_TAG, "Found location setting");
            int locationIndex = cursor.getColumnIndex(LocationEntry._ID);
            locationRowId = cursor.getLong(locationIndex);
        } else {
            Log.i(LOG_TAG, "Inserting location setting");
            ContentValues values = new ContentValues();
            values.put(LocationEntry.COLUMN_LOCATION_SETTING, locationSetting);
            values.put(LocationEntry.COLUMN_CITY_NAME, cityName);
            values.put(LocationEntry.COLUMN_COORD_LAT, lat);
            values.put(LocationEntry.COLUMN_COORD_LONG, lon);

            Uri returnUri = getContext().getContentResolver().insert(
                    WeatherContract.LocationEntry.CONTENT_URI, values);

            locationRowId = ContentUris.parseId(returnUri);
        }

        cursor.close();
        return locationRowId;
    }

    /**
     * Notification
     */
    private void notifyWeather() {
        Context context = getContext();
        // checking the last update and notify if it' the first of the day
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(context);

        String displayNotificationsKey = context.getString(R.string.pref_enable_notifications_key);
        boolean displayNotifications = prefs
                .getBoolean(
                        displayNotificationsKey,
                        Boolean.parseBoolean(context
                                .getString(R.string.pref_enable_notifications_default)));

        if (displayNotifications) {

            String lastNotificationKey = context.getString(R.string.pref_last_notification);
            long lastSync = prefs.getLong(lastNotificationKey, 0);
            boolean isMetric = Utility.isMetric(context);

            if (System.currentTimeMillis() - lastSync >= DAY_IN_MILLIS) {
                // Last sync was more than 1 day ago, let's send a notification
                // with
                // the weather.
                String locationQuery = Utility.getPreferredLocation(context);

                Uri weatherUri = WeatherEntry.buildWeatherLocationWithDate(
                        locationQuery,
                        WeatherContract.getDbDateString(new Date()));

                // we'll query our contentProvider, as always
                Cursor cursor = context.getContentResolver().query(weatherUri,
                        NOTIFY_WEATHER_PROJECTION, null, null, null);

                if (cursor.moveToFirst()) {
                    int weatherId = cursor.getInt(INDEX_WEATHER_ID);
                    double high = cursor.getDouble(INDEX_MAX_TEMP);
                    double low = cursor.getDouble(INDEX_MIN_TEMP);
                    String desc = cursor.getString(INDEX_SHORT_DESC);

                    int iconId = Utility
                            .getIconResourceForWeatherCondition(weatherId);
                    String title = context.getString(R.string.app_name);

                    // Define the text of the forecast.
                    String contentText = String.format(
                            context.getString(R.string.format_notification),
                            desc,
                            Utility.formatTemperature(context, high, isMetric),
                            Utility.formatTemperature(context, low, isMetric));

                    // build your notification here.
                    // NotificationCompatBuilder is a very convenient way to
                    // build
                    // backward-compatible
                    // notifications. Just throw in some data.
                    NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(
                            context).setSmallIcon(iconId)
                            .setContentTitle(title).setContentText(contentText);

                    // Make something interesting happen when the user clicks on
                    // the notification.
                    // In this case, opening the app is sufficient.
                    Intent resultIntent = new Intent(context,
                            MainActivity.class);

                    // The stack builder object will contain an artificial back
                    // stack for the started Activity.
                    // This ensures that navigating backward from the Activity
                    // leads out of
                    // your application to the Home screen.
                    TaskStackBuilder stackBuilder = TaskStackBuilder
                            .create(context);
                    stackBuilder.addNextIntent(resultIntent);
                    PendingIntent resultPendingIntent = stackBuilder
                            .getPendingIntent(0,
                                    PendingIntent.FLAG_UPDATE_CURRENT);

                    mBuilder.setContentIntent(resultPendingIntent);
                    NotificationManager mNotificationManager = (NotificationManager) context
                            .getSystemService(Context.NOTIFICATION_SERVICE);

                    // WEATHER_NOTIFICATION_ID allows you to update the
                    // notification later on.
                    mNotificationManager.notify(WEATHER_NOTIFICATION_ID, mBuilder.build());

                    // refreshing last sync
                    SharedPreferences.Editor editor = prefs.edit();
                    editor.putLong(lastNotificationKey, System.currentTimeMillis());
                    editor.commit();
                }
            }
        }
    }

}

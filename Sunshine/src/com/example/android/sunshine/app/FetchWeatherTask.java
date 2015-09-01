/**
 * 
 */
package com.example.android.sunshine.app;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.Vector;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.example.android.sunshine.app.data.WeatherContract;
import com.example.android.sunshine.app.data.WeatherContract.LocationEntry;
import com.example.android.sunshine.app.data.WeatherContract.WeatherEntry;

import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.net.Uri.Builder;
import android.os.AsyncTask;
import android.preference.PreferenceManager;
import android.util.Log;
import android.widget.ArrayAdapter;

/**
 * This is a fetch weather task.
 * 
 */
public class FetchWeatherTask extends AsyncTask<String, Void, Void> {

	private final String LOG_TAG = FetchWeatherTask.class.getSimpleName();

	private ArrayAdapter<String> mForecastAdapter;
	private final Context mContext;
	
	public FetchWeatherTask(Context context) {
		mContext = context;
		mForecastAdapter = new ArrayAdapter<String>(context, R.layout.list_item_forecast);
	}

	public FetchWeatherTask(Context context, ArrayAdapter<String> arrayAdapter) {
		mContext = context;
		mForecastAdapter = arrayAdapter;
	}

	/**
	 * @param String... params - 0th postal code, 1st temperature unit
	 *            "http://api.openweathermap.org/data/2.5/forecast/daily?q=94043&mode=json&units=metric&cnt=7"
	 */
	@Override
	protected Void doInBackground(String... inputs) {

		// If there's no zip code, there's nothing to look up. Verify size of params.
		if (null == inputs || inputs.length == 0) {
			return null;
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
		String locationQuery = inputs[0];// , units = inputs[1];

		try {
			final String FORECAST_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast/daily?";
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

		return null;
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
		// For presentation, assume the user doesn't care about tenths of a
		// degree.

		Log.i(LOG_TAG, String.format("Before %s %s", high, low));

		SharedPreferences sharedPreferences = PreferenceManager
				.getDefaultSharedPreferences(mContext);

		String temperatureUnit = sharedPreferences.getString(
				mContext.getString(R.string.pref_temperature_unit_key),
				mContext.getString(R.string.pref_temperature_default_metric));

		Log.i(LOG_TAG, "--- Temperature Unit " + temperatureUnit);

		if (temperatureUnit.equalsIgnoreCase(mContext
				.getString(R.string.pref_temperature_imperial))) {
			high = ((high * 9) / 5) + 32;
			low = ((low * 9) / 5) + 32;
		} else if (!temperatureUnit.equalsIgnoreCase(mContext
				.getString(R.string.pref_temperature_default_metric))) {
			Log.d(LOG_TAG, "Unit not found + " + temperatureUnit);
		}

		long roundedHigh = Math.round(high);
		long roundedLow = Math.round(low);

		Log.i(LOG_TAG, String.format("After %s %s", roundedHigh, roundedLow));

		String highLowStr = roundedHigh + "/" + roundedLow;
		return highLowStr;
	}

	/**
	 * Take the String representing the complete forecast in JSON Format and
	 * pull out the data we need to construct the Strings needed for the
	 * wireframes.
	 * 
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
			
			mContext.getContentResolver().delete(WeatherEntry.CONTENT_URI, null, null);
			
			ContentValues[] values = cVector.toArray(new ContentValues[cVector.size()]);
			long rowsInserted = mContext.getContentResolver().bulkInsert(WeatherEntry.CONTENT_URI, values);
			Log.v(LOG_TAG, "inserted " + rowsInserted + " rows of weather data");
		}
		
		return resultStrs;
	}

//	@Override
//	protected void onPostExecute(String[] result) {
//		// TODO Auto-generated method stub
//		// super.onPostExecute(result);
//		if (null != result) {
//			mForecastAdapter.clear();
//			for (String s : result) {
//				Log.i(LOG_TAG, " --- forecast data : " + s);
//				mForecastAdapter.add(s);
//			}
//		}
//	}

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

		Cursor cursor = mContext.getContentResolver().query(
				LocationEntry.CONTENT_URI,
				new String[] { WeatherContract.LocationEntry._ID },
				LocationEntry.COLUMN_LOCATION_SETTING + " = ?",
				new String[] { locationSetting }, null);
		
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

			Uri returnUri = mContext.getContentResolver().insert(
					WeatherContract.LocationEntry.CONTENT_URI, values);

			locationRowId = ContentUris.parseId(returnUri);
		}
		
		cursor.close();
		return locationRowId;
	}
	
	/** 
	 * @param String locationSetting
	 * @param ContentValues[] values
	 * @return number of weather data rows inserted
	 */
//	private boolean DEBUG = true;
//	private long addWeather(String locationSetting, ContentValues[] values) {
//		
//		Log.i(LOG_TAG, "Inserting weather of location " + locationSetting);
//		
//		Uri uri = WeatherEntry.buildWeatherLocation(locationSetting);
//		
//		Cursor cursor = mContext.getContentResolver().query(uri, null, null, null, null);
//		
//		if (cursor.moveToFirst()) {
//			mContext.getContentResolver().delete(uri, WeatherEntry.COLUMN_LOC_KEY + " = ?", new String[]{locationSetting});
//		}
//		
//		cursor.close();
//		return mContext.getContentResolver().bulkInsert(uri, values);
//	}
}

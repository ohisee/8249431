/**
 * 
 */
package com.example.android.sunshine.app;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import android.app.AlarmManager;
import android.app.IntentService;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.net.Uri.Builder;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.SystemClock;
import android.preference.PreferenceManager;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.app.LoaderManager.LoaderCallbacks;
import android.support.v4.content.Loader;
import android.support.v4.content.CursorLoader;
import android.support.v4.widget.SimpleCursorAdapter;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebChromeClient.CustomViewCallback;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.example.android.sunshine.app.data.WeatherContract;
import com.example.android.sunshine.app.data.WeatherContract.LocationEntry;
import com.example.android.sunshine.app.data.WeatherContract.WeatherEntry;
import com.example.android.sunshine.service.SunshineService;
import com.example.android.sunshine.sync.SunshineSyncAdapter;


/**
 * Represents forecast fragment, a placeholder fragment containing a simple view.
 * 
 */
public class ForecastFragment extends Fragment implements LoaderCallbacks<Cursor> {
	
	private String mLocation;
	private static final int FORECAST_LOADER = 0;
	
	private static final String SELECTED_DATE_KEY = "selected_date";
	
	private final String LOG_TAG = ForecastFragment.class.getSimpleName();
	
	// Query column
	private static final String[] FORECASR_COLUMNS = {
		WeatherEntry.TABLE_NAME + "." + WeatherEntry._ID,
		WeatherEntry.COLUMN_DATETEXT,
		WeatherEntry.COLUMN_SHORT_DESC,
		WeatherEntry.COLUMN_MAX_TEMP,
		WeatherEntry.COLUMN_MIN_TEMP,
		WeatherEntry.COLUMN_WEATHER_ID,
		LocationEntry.COLUMN_LOCATION_SETTING,
		LocationEntry.COLUMN_COORD_LAT,
		LocationEntry.COLUMN_COORD_LONG
	};
	
	// These indices are tied to FORECAST_COLUMNS. If FORECAST_COLUMNs changes, these must change.
	public static final int COL_WEATHER_ENTRY_ID = 0;
	public static final int COL_WEATHER_DATE = 1;
	public static final int COL_WEATHER_DESC = 2;
	public static final int COL_WEATHER_MAX_TEMP = 3;
	public static final int COL_WEATHER_MIN_TEMP = 4;
	public static final int COL_WEATHER_ID = 5;
	public static final int COL_LOCATION_SETTING = 6;
	public static final int COL_LOCATION_LAT = 7;
	public static final int COL_LOCATION_LONG = 8;
	
	//private ArrayAdapter<String> mForecastAdapter;
	//private SimpleCursorAdapter mForecastCursorAdapter;
	private ForecastAdapter mForecastAdapter;
	
	private int mPosition;
	
	private ListView mListView;
	
	private boolean mUseTodayLayout;
	
	/**
	 * A callback interface that all activities containing this fragment must
	 * implement. This mechanism allows activities to be notified of item
	 * selections.
	 */
	public interface Callback {
		/**
		 * Callback for when an item has been selected.
		 */
		public void onItemSelected(String date);
	}
	
	public ForecastFragment() {
    }
	
    @Override
	public void onActivityCreated(@Nullable Bundle savedInstanceState) {
		getLoaderManager().initLoader(FORECAST_LOADER, null, this);
		super.onActivityCreated(savedInstanceState);
	}
    
	/**
     * Must use this in order to see menu items (enable menu).
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
    	super.onCreate(savedInstanceState);
    	// Must call this for this fragment to handle menu events.
    	setHasOptionsMenu(true);
    }

    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
    	inflater.inflate(R.menu.forecastfragment, menu);
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
    	switch(item.getItemId()) {
    		case R.id.action_refresh:
    			fetchAndUpdateWeather();
				return true;
    		case R.id.action_settings:
    			return true;
    		case R.id.action_map:
    			fetchPreferredLocation();
    			return true;
    		default:
    			return super.onOptionsItemSelected(item);
    	}
    }
    
    /**
     * Fetch and update weather.
     */
    private void fetchAndUpdateWeather() {
//		SharedPreferences sharedPreferences = PreferenceManager
//				.getDefaultSharedPreferences(getActivity());
//		String preferredLocation = sharedPreferences.getString(
//				getString(R.string.pref_location_key),
//				getString(R.string.pref_location_default));
//		String temperatureUnit = sharedPreferences.getString(
//				getString(R.string.pref_temperature_unit_key),
//				getString(R.string.pref_temperature_default_metric));
    	
		//String preferredLocation = Utility.getPreferredLocation(getActivity());
		//Log.i(LOG_TAG, String.format("Preferred Location %s ", preferredLocation));
		//FetchWeatherTask fetchWeatherTask = new FetchWeatherTask(getActivity());
		//fetchWeatherTask.execute(preferredLocation);
		
    	//Intent intent = new Intent(getActivity(), SunshineService.class);
    	//intent.putExtra(SunshineService.LOCATION_QUERY_EXTRA, preferredLocation);
    	//getActivity().startService(intent);
    	
    	//Intent alarmIntent = new Intent(getActivity(), SunshineService.AlarmReceiver.class);
    	//alarmIntent.putExtra(SunshineService.LOCATION_QUERY_EXTRA, preferredLocation);
		//AlarmManager alarmManager = (AlarmManager) getActivity().getSystemService(Context.ALARM_SERVICE);
		//PendingIntent pendingIntent = PendingIntent.getBroadcast(getActivity(), 0, alarmIntent, PendingIntent.FLAG_ONE_SHOT); // one shot
		// Wake up the device to fire a one-time (non-repeating) alarm in 5 seconds
		//alarmManager.set(AlarmManager.ELAPSED_REALTIME_WAKEUP,
		//		SystemClock.elapsedRealtime() + 5 * 1000, pendingIntent);
		//alarmManager.set(AlarmManager.RTC_WAKEUP, SystemClock.elapsedRealtime() + 5000, pendingIntent);
    	
    	SunshineSyncAdapter.syncImmediately(getActivity());
    }
    
    /**
     * Fragment on start.
     */
    @Override
	public void onStart() {
		super.onStart();
		// Not to call fetchAndUpdateWeather after using loader
		//fetchAndUpdateWeather();
	}
    
    /**
     * Fragment on resume.
     */
	@Override
	public void onResume() {
		super.onResume();
		// Check weather to load / fetch new weather data
		if (null != mLocation && !mLocation.equals(Utility.getPreferredLocation(getActivity()))) {
			// Cannot just call fetchAndUpdateWeather method
			// Must go through loader manager, restart loader, to fetch and load new weather data into cursor
			getLoaderManager().restartLoader(FORECAST_LOADER, null, this);
		}
	}
	
	public void setUseTodayLayout(boolean useTodayLayout) {
		mUseTodayLayout = useTodayLayout;
		if (null != mForecastAdapter) {
			mForecastAdapter.setUserTodayLayout(mUseTodayLayout);
		}
	}

	@Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
            final Bundle savedInstanceState) {
		
//		mForecastCursorAdapter = new SimpleCursorAdapter(getActivity(),
//				R.layout.list_item_forecast, 
//				null, 
//				new String[] {
//						WeatherEntry.COLUMN_DATETEXT,
//						WeatherEntry.COLUMN_SHORT_DESC,
//						WeatherEntry.COLUMN_MAX_TEMP,
//						WeatherEntry.COLUMN_MIN_TEMP },
//				new int[] {
//						R.id.list_item_date_textview,
//						R.id.list_item_forecast_textview,
//						R.id.list_item_high_textview,
//						R.id.list_item_low_textview }, 
//				0);
		
//		mForecastCursorAdapter.setViewBinder(new SimpleCursorAdapter.ViewBinder() {
//					@Override
//					public boolean setViewValue(View view, Cursor cursor, int columnIndex) {
//						boolean isMetric = Utility.isMetric(getActivity());
//						switch (columnIndex) {
//							case COL_WEATHER_MAX_TEMP:
//							case COL_WEATHER_MIN_TEMP: {
//								((TextView) view).setText(Utility.formatTemperature(
//												cursor.getDouble(columnIndex), isMetric));
//								return true;
//							}
//							case COL_WEATHER_DATE: {
//								String dateString = cursor.getString(columnIndex);
//								TextView dateView = (TextView) view;
//								dateView.setText(Utility.formatDate(dateString));
//								return true;
//							}
//						}
//						return false;
//					}
//				});
		
        View rootView = inflater.inflate(R.layout.fragment_main, container, false);
        
//		List<String> weekForecast = new ArrayList<String>(Arrays.asList(
//				"Today - Sunnny - 88/63", "Tomorrow - Foggy - 70/46",
//				"Weds - Cloudy - 72/63", "Thurs - Rainy - 64/51",
//				"Fri - Foggy - 70/46", "Sat - Sunny - 76/68"));
	
//		ArrayAdapter<String> arrayWeekForecastAdapter = new ArrayAdapter<String>(
//				getActivity(), R.layout.list_item_forecast,
//				R.id.list_item_forecast_textview, weekForecast);
		
//		mForecastAdapter = new ArrayAdapter<String>(
//				getActivity(),
//				R.layout.list_item_forecast, 
//				R.id.list_item_forecast_textview,
//				weekForecast);
        
//		mForecastAdapter = new ArrayAdapter<String>(getActivity(),
//				R.layout.list_item_forecast_textview_only, R.id.list_item_forecast_textview,
//				new ArrayList<String>()); // pass an empty array list of String type
			
		//ListView listView = (ListView) rootView.findViewById(R.id.listview_forecast);
        mListView = (ListView) rootView.findViewById(R.id.listview_forecast);
//		listView.setAdapter(arrayWeekForecastAdapter);
		//listView.setAdapter(mForecastCursorAdapter);
        mForecastAdapter = new ForecastAdapter(getActivity(), null, 0);
        mForecastAdapter.setUserTodayLayout(mUseTodayLayout);
		mListView.setAdapter(mForecastAdapter);
		mListView.setOnItemClickListener(new OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
//				String weatherForecast = mForecastAdapter.getItem(position);
//				Toast.makeText(getActivity(), weatherForecast, Toast.LENGTH_SHORT).show();
//				Intent explicitIntent = new Intent(getActivity(),
//						DetailActivity.class).putExtra(Intent.EXTRA_TEXT,
//						weatherForecast);
//				startActivity(explicitIntent);
				//SimpleCursorAdapter simpleCursorAdapter = (SimpleCursorAdapter) parent.getAdapter();
				//Cursor cursor = simpleCursorAdapter.getCursor();
				ForecastAdapter forecastAdapter = (ForecastAdapter) parent.getAdapter();
				Cursor cursor = forecastAdapter.getCursor();
				if (null != cursor && cursor.moveToPosition(position)) {
					boolean isMetric = Utility.isMetric(getActivity());
					String forcast = String.format("%s - %s - %s / %s", 
							Utility.formatDate(cursor.getString(COL_WEATHER_DATE)),
							cursor.getString(COL_WEATHER_DESC), 
							Utility.formatTemperature(cursor.getDouble(COL_WEATHER_MAX_TEMP), isMetric), 
							Utility.formatTemperature(cursor.getDouble(COL_WEATHER_MIN_TEMP), isMetric));
					Toast.makeText(getActivity(), forcast, Toast.LENGTH_SHORT).show();
					//String date = Utility.formatDate(cursor.getString(COL_WEATHER_DATE));
					// No need to get the formatted string since will use its as Uri
					String date = cursor.getString(COL_WEATHER_DATE);
//					Intent explicitIntent = new Intent(getActivity(),
//							DetailActivity.class).putExtra(Intent.EXTRA_TEXT,
//							forcast);
//					Intent explicitIntent = new Intent(getActivity(),
//							DetailActivity.class).putExtra(DetailActivity.DATE_KEY, date);
//					startActivity(explicitIntent);
					
					//((Callback) getActivity()).onItemSelected(cursor.getString(COL_WEATHER_DATE));
					((Callback) getActivity()).onItemSelected(date);
				}
				//cursor.close();
				mPosition = position;
			}
		});
		
		// Get position from saved instance state
		if (null != savedInstanceState && savedInstanceState.containsKey(SELECTED_DATE_KEY)) {
			mPosition = savedInstanceState.getInt(SELECTED_DATE_KEY);
		}
		
        return rootView;
    }
	
	@Override
	public void onSaveInstanceState(Bundle outState) {
		if (mPosition != ListView.INVALID_POSITION) {
			outState.putInt(SELECTED_DATE_KEY, mPosition);
		}
		super.onSaveInstanceState(outState);
	}

	// Support loader manager's loader callbacks.
	@Override
	public Loader<Cursor> onCreateLoader(int id, Bundle args) {
		// This is called when a new Loader needs to be created. This
		// fragment only uses one loader, so we don't care about checking the
		// id.

		// To only show current and future dates, get the String representation
		// for today,
		// and filter the query to return weather only for dates after or
		// including today.
		// Only return data after today.
		String startDate = WeatherContract.getDbDateString(new Date());

		// Sort order: Ascending, by date.
		String sortOrder = WeatherEntry.COLUMN_DATETEXT + " ASC";

		mLocation = Utility.getPreferredLocation(getActivity());
		Uri weatherForLocationUri = WeatherEntry.buildWeatherLocationWithStartDate(
				mLocation, startDate);
		
		Log.d(LOG_TAG, "Uri " + weatherForLocationUri.toString());

		// Now create and return a CursorLoader that will take care of
		// creating a Cursor for the data being displayed.
		return new CursorLoader(getActivity(), weatherForLocationUri,
				FORECASR_COLUMNS, null, null, sortOrder);
	}

	@Override
	public void onLoadFinished(Loader<Cursor> loader, Cursor data) {
		mForecastAdapter.swapCursor(data);
		if (mPosition != ListView.INVALID_POSITION) {
			mListView.setSelection(mPosition);
		}
	}

	@Override
	public void onLoaderReset(Loader<Cursor> loader) {
		mForecastAdapter.swapCursor(null);
	}
	
	/**
	 * Using the URI scheme for showing a location found on a map. This super-handy 
	 * intent can is detailed in the "Common Intents" page of Android's developer site: 
	 * http://developer.android.com/guide/components/intents-common.html#Maps
	 * geo:latitude,longitude
	 */
	private void fetchPreferredLocation() {
		if (null != mForecastAdapter) {
			Cursor cursor = mForecastAdapter.getCursor();

			if (null != cursor && cursor.moveToPosition(0)) {

				String positionLat = cursor.getString(COL_LOCATION_LAT);
				String positionLong = cursor.getString(COL_LOCATION_LONG);
				Uri geoLocation = Uri.parse("geo:" + positionLat + ","
						+ positionLong);

				Intent intent = new Intent(Intent.ACTION_VIEW);
				intent.setData(geoLocation);
				if (intent.resolveActivity(getActivity().getPackageManager()) != null) {
					startActivity(intent);
				} else {
					Log.d(LOG_TAG, "Couldn't call " + geoLocation.toString() + ", no receiving apps installed!");
				}
			}
		}
	}
	

	
    /**
     * Represents fetch whether task.
     * ****************** Not being used **********************
     */
    public class InnerFetchWeatherTask extends AsyncTask<String, Void, String[]> {
    	
    	private final String LOG_TAG = InnerFetchWeatherTask.class.getSimpleName();
    	
    	/**
    	 * @param String... params - 0th postal code, 1st temperature unit
    	 * "http://api.openweathermap.org/data/2.5/forecast/daily?q=94043&mode=json&units=metric&cnt=7"
    	 */
		@Override
		protected String[] doInBackground(String... inputs) {
			// These two need to be declared outside the try/catch
			// so that they can be closed in the finally block.
			HttpURLConnection urlConnection = null;
			BufferedReader reader = null;
			// Will contain the raw JSON response as a string.
			String forecastJsonStr = null;
			
			String format = "json";
			String units = "metric";
			int daysCount = 7;
			String postalCode = inputs[0];//, units = inputs[1];

			try {
				// Build forecast data URL
				Builder uriBuilder = new Builder();
				uriBuilder.scheme("http").authority("api.openweathermap.org")
						.appendPath("data").appendPath("2.5")
						.appendPath("forecast").appendPath("daily")
						.appendQueryParameter("q", postalCode)
						.appendQueryParameter("mode", format)
						.appendQueryParameter("units", units)
						.appendQueryParameter("cnt", Integer.toString(daysCount)).build();
				
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
				//Log.i(LOG_TAG,  forecastJsonStr);
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
					return getWeatherDataFromJson(forecastJsonStr, daysCount);
				} catch (JSONException e) {
					Log.e(LOG_TAG, "Error getting weather data " + e.getMessage(), e);
				}
			}
			
			return null;
		}
		
		/**
		 * The date/time conversion code is going to be moved outside the
		 * asynctask later, so for convenience we're breaking it out into its
		 * own method now.
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
					.getDefaultSharedPreferences(getActivity());
			
			String temperatureUnit = sharedPreferences.getString(
					getString(R.string.pref_temperature_unit_key),
					getString(R.string.pref_temperature_default_metric));
			
			Log.i(LOG_TAG, "--- Temperature Unit " + temperatureUnit);
			
			if (temperatureUnit.equalsIgnoreCase(getString(R.string.pref_temperature_imperial))) {
				high = ((high * 9) / 5) + 32;
				low = ((low * 9) / 5) + 32;
			} else if (!temperatureUnit.equalsIgnoreCase(getString(R.string.pref_temperature_default_metric))) {
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
				int numDays) throws JSONException {

			// These are the names of the JSON objects that need to be
			// extracted.
			final String OWM_LIST = "list";
			final String OWM_WEATHER = "weather";
			final String OWM_TEMPERATURE = "temp";
			final String OWM_MAX = "max";
			final String OWM_MIN = "min";
			final String OWM_DATETIME = "dt";
			final String OWM_DESCRIPTION = "main";
			final String OWN_CITY = "city";
			final String OWN_COORD = "coord";

			JSONObject forecastJson = new JSONObject(forecastJsonStr);
			JSONArray weatherArray = forecastJson.getJSONArray(OWM_LIST);

			String[] resultStrs = new String[numDays];
			for (int i = 0; i < weatherArray.length(); i++) {
				// For now, using the format "Day, description, hi/low"
				String day;
				String description;
				String highAndLow;

				// Get the JSON object representing the day
				JSONObject dayForecast = weatherArray.getJSONObject(i);

				// The date/time is returned as a long. We need to convert that
				// into something human-readable, since most people won't read
				// "1400356800" as
				// "this saturday".
				long dateTime = dayForecast.getLong(OWM_DATETIME);
				day = getReadableDateString(dateTime);

				// description is in a child array called "weather", which is 1
				// element long.
				JSONObject weatherObject = dayForecast
						.getJSONArray(OWM_WEATHER).getJSONObject(0);
				description = weatherObject.getString(OWM_DESCRIPTION);

				// Temperatures are in a child object called "temp". Try not to
				// name variables
				// "temp" when working with temperature. It confuses everybody.
				JSONObject temperatureObject = dayForecast
						.getJSONObject(OWM_TEMPERATURE);
				double high = temperatureObject.getDouble(OWM_MAX);
				double low = temperatureObject.getDouble(OWM_MIN);

				highAndLow = formatHighLows(high, low);
				resultStrs[i] = day + " - " + description + " - " + highAndLow;
			}

			return resultStrs;
		}

		@Override
		protected void onPostExecute(String[] result) {
			//super.onPostExecute(result);
//			if (null != result) {
//				mForecastAdapter.clear();
//				for (String s : result) {
//					Log.i(LOG_TAG, " --- forecast data : " + s);
//					mForecastAdapter.add(s);
//				}
//			}
		}
    }
}

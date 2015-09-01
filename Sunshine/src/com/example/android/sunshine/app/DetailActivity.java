package com.example.android.sunshine.app;

import com.example.android.sunshine.app.data.WeatherContract.LocationEntry;
import com.example.android.sunshine.app.data.WeatherContract.WeatherEntry;

import android.support.annotation.Nullable;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v7.widget.ShareActionProvider;
import android.support.v4.app.Fragment;
import android.support.v4.app.LoaderManager.LoaderCallbacks;
import android.support.v4.content.CursorLoader;
import android.support.v4.content.Loader;
import android.support.v4.view.MenuItemCompat;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.os.Build;

public class DetailActivity extends ActionBarActivity {
	
	private static final int DETAIL_LOADER = 0;
	public static final String DATE_KEY = "forecast_date";
	public static final String LOCATION_KEY = "location";
	
	private final String LOG_TAG = DetailActivity.class.getSimpleName();

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_detail);
		if (savedInstanceState == null) {
//			getSupportFragmentManager().beginTransaction()
//					.add(R.id.container, new DetailFragment()).commit();
			// Create the detail fragment and add it to the activity using a fragment transaction
			String date = getIntent().getStringExtra(DATE_KEY);

			Bundle bundleArguments = new Bundle();
			bundleArguments.putString(DATE_KEY, date);

			DetailFragment detailFragment = new DetailFragment();
			detailFragment.setArguments(bundleArguments);

			// Dynamically add the detail fragment to the container
			getSupportFragmentManager().beginTransaction()
					.add(R.id.weather_detail_container, detailFragment)
					.commit();
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.detail, menu);
		return true;
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
        	Intent settingsIntent = new Intent(this, SettingsActivity.class);
        	startActivity(settingsIntent);
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	/**
	 * A placeholder fragment containing a simple view.
	 * *************** Not being used ****************
	 */
	public static class InnerDetailFragment extends Fragment implements LoaderCallbacks<Cursor> {
		
		private final String LOG_TAG = DetailFragment.class.getSimpleName();
		
		private final String SUNSHINE_SHARE_HASHTAG = " #SunshineApp";
		
		private ShareActionProvider mShareActionProvider;
		
		private String mForecastString;
		
		private String mLocation;

		public InnerDetailFragment() {
			super.setHasOptionsMenu(true);
		}
		
		@Override
		public void onActivityCreated(@Nullable Bundle savedInstanceState) {
			getLoaderManager().initLoader(DETAIL_LOADER, null, this);
			if (null != savedInstanceState) {
				mLocation = savedInstanceState.getString(LOCATION_KEY);
			}
			super.onActivityCreated(savedInstanceState);
		}

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater.inflate(R.layout.fragment_detail,
					container, false);
			
//			Intent weatherIntent = getActivity().getIntent();
//			if (null != weatherIntent && weatherIntent.hasExtra(Intent.EXTRA_TEXT)) {
//				String message = weatherIntent.getStringExtra(Intent.EXTRA_TEXT);
//				mForecastString = weatherIntent.getStringExtra(Intent.EXTRA_TEXT);
//				TextView tv = (TextView) rootView.findViewById(R.id.details);
//				tv.setText(message);
//				tv.setText(mForecastString);
//			}
			
			return rootView;
		}

		/**
		 * @param Menu menu
		 * @param MenuInflater inflater
		 */
		@Override
		public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
			// Inflate detail fragment menu
			inflater.inflate(R.menu.detailfragment, menu);
			
			// Get detail fragment menu item
			MenuItem shareItem = menu.findItem(R.id.action_share);

			// Get share action provider
			mShareActionProvider = (ShareActionProvider) MenuItemCompat
					.getActionProvider(shareItem);
			
			// Attach an intent to this share action provider 
			if (null != mShareActionProvider) {
				mShareActionProvider.setShareIntent(createShareForecastIntent());
			} else {
				Log.i(LOG_TAG, "Share action provider is not good for use");
			}
		}

		/**
		 * @return an intent
		 */
		private Intent createShareForecastIntent() {
			Intent shareIntent = new Intent(Intent.ACTION_SEND);
			shareIntent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_WHEN_TASK_RESET);
			shareIntent.setType("text/plain");
			shareIntent.putExtra(Intent.EXTRA_TEXT,
					new StringBuilder((null == mForecastString) ? ""
							: mForecastString).append(SUNSHINE_SHARE_HASHTAG)
							.toString());
			return shareIntent;
		}
		
		/**
		 * Preserve location
		 */
		@Override
		public void onSaveInstanceState(Bundle outState) {
			if (null != mLocation) {
				outState.putString(LOCATION_KEY, mLocation);
			}
			super.onSaveInstanceState(outState);
		}
		
		/**
		 * Resume
		 */
		@Override
		public void onResume() {
			super.onResume();
			if (null != mLocation && !mLocation.equals(Utility.getPreferredLocation(getActivity()))) {
				getLoaderManager().restartLoader(DETAIL_LOADER, null, this);
			}
		}

		@Override
		public Loader<Cursor> onCreateLoader(int id, Bundle args) {
			
			Intent intent = getActivity().getIntent();
			
			if (null == intent || !intent.hasExtra(DATE_KEY)) {
				return null;
			}
			
			//String dateString = getActivity().getIntent().getStringExtra(DATE_KEY);
			
			String dateString = intent.getStringExtra(DATE_KEY);
			
			// Query column
			final String[] FORECASR_DETAILS_COLUMNS = {
				WeatherEntry.TABLE_NAME + "." + WeatherEntry._ID,
				WeatherEntry.COLUMN_DATETEXT,
				WeatherEntry.COLUMN_SHORT_DESC,
				WeatherEntry.COLUMN_MAX_TEMP,
				WeatherEntry.COLUMN_MIN_TEMP,
				WeatherEntry.COLUMN_HUMIDITY,
				WeatherEntry.COLUMN_PRESSURE,
				WeatherEntry.COLUMN_WIND_SPEED,
				WeatherEntry.COLUMN_DEGREES,
				WeatherEntry.COLUMN_WEATHER_ID,
				LocationEntry.COLUMN_LOCATION_SETTING
			};
			
			// Sort order: Ascending, by date.
			String sortOrder = WeatherEntry.COLUMN_DATETEXT + " ASC";
			
			mLocation = Utility.getPreferredLocation(getActivity());
			Uri weatherUri = WeatherEntry.buildWeatherLocationWithDate(mLocation, dateString);
			
			Log.i(LOG_TAG, "Uri " + weatherUri.toString());
			
			return new CursorLoader(getActivity(), weatherUri,
					FORECASR_DETAILS_COLUMNS, null, null, sortOrder);
		}

		@Override
		public void onLoadFinished(Loader<Cursor> loader, Cursor data) {
			
			if (data.moveToFirst()) {
				 
				String dateString = Utility.formatDate(
				data.getString(data.getColumnIndex(WeatherEntry.COLUMN_DATETEXT)));
				String weatherDescription =
				data.getString(data.getColumnIndex(WeatherEntry.COLUMN_SHORT_DESC));
				 
				boolean isMetric = Utility.isMetric(getActivity());
				String high = Utility.formatTemperature(
				data.getDouble(data.getColumnIndex(WeatherEntry.COLUMN_MAX_TEMP)), isMetric);
				String low = Utility.formatTemperature(
				data.getDouble(data.getColumnIndex(WeatherEntry.COLUMN_MIN_TEMP)), isMetric);
				 
				((TextView) getView().findViewById(R.id.detail_date_textview)).setText(dateString);
				((TextView) getView().findViewById(R.id.detail_forecast_textview)).setText(weatherDescription);
				//((TextView) getView().findViewById(R.id.detail_high_textview)).setText(high + "\u00B0");
				((TextView) getView().findViewById(R.id.detail_high_textview)).setText(high);
				//((TextView) getView().findViewById(R.id.detail_low_textview)).setText(low + "\u00B0");
				((TextView) getView().findViewById(R.id.detail_high_textview)).setText(high);
				
				mForecastString = String.format("%s - %s - %s / %s",
				dateString, weatherDescription, high, low);
				 
				Log.v(LOG_TAG, "Forecast String: " + mForecastString);
				
				if (null != mShareActionProvider) {
					mShareActionProvider.setShareIntent(createShareForecastIntent());
				}
			}
		}

		@Override
		public void onLoaderReset(Loader<Cursor> loader) {
			getLoaderManager().restartLoader(DETAIL_LOADER, null, this);
		}
	}
}

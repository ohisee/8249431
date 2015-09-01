/**
 * 
 */
package com.example.android.sunshine.app;

import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.support.v4.app.LoaderManager.LoaderCallbacks;
import android.support.v4.content.CursorLoader;
import android.support.v4.content.Loader;
import android.support.v4.view.MenuItemCompat;
import android.support.v7.widget.ShareActionProvider;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.android.sunshine.app.data.WeatherContract.LocationEntry;
import com.example.android.sunshine.app.data.WeatherContract.WeatherEntry;

/**
 * Represents detail fragment.
 *
 */
public class DetailFragment extends Fragment implements LoaderCallbacks<Cursor> {
	
	private final String LOG_TAG = DetailFragment.class.getSimpleName();
	
	private final String SUNSHINE_SHARE_HASHTAG = " #SunshineApp";
	
	private ShareActionProvider mShareActionProvider;
	
	private String mForecastString;
	
	private String mLocation;
	
	private static final int DETAIL_LOADER = 0;
	public static final String DATE_KEY = "forecast_date";
	public static final String LOCATION_KEY = "location";
	
	private ImageView mIconView;
	private TextView mDayView;
	private TextView mDateView;
	private TextView mForecastDescriptionView;
	private TextView mHighTempView;
	private TextView mLowTempView;
	private TextView mWindSpeedView;
	private TextView mHumidityView;
	private TextView mPressureView;
	private WindDirectionView mMyView;
	

	public DetailFragment() {
		super.setHasOptionsMenu(true);
	}
	
	@Override
	public void onActivityCreated(@Nullable Bundle savedInstanceState) {
		super.onActivityCreated(savedInstanceState);
		if (null != savedInstanceState) {
			mLocation = savedInstanceState.getString(LOCATION_KEY);
		}
//		Intent intent = getActivity().getIntent();
//		if (intent != null && intent.hasExtra(DATE_KEY)) {
//			getLoaderManager().initLoader(DETAIL_LOADER, null, this);
//		}
		// No more depending on the Intent
		// Switch to use Bundle arguments
		Bundle arguments = getArguments();
		if (null != arguments && arguments.containsKey(DATE_KEY)) {
			getLoaderManager().initLoader(DETAIL_LOADER, null, this);
		}
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.forecast_detail, container, false);
		mIconView = (ImageView) rootView.findViewById(R.id.forecast_detail_icon);
		mDayView = (TextView) rootView.findViewById(R.id.forecast_detail_day_textview);
		mDateView = (TextView) rootView.findViewById(R.id.forecast_detail_date_textview);
		mForecastDescriptionView = (TextView) rootView.findViewById(R.id.forecast_detail_forecast_textview);
		mHighTempView = (TextView) rootView.findViewById(R.id.forecast_detail_high_textview);
		mLowTempView = (TextView) rootView.findViewById(R.id.forecast_detail_low_textview);
		mWindSpeedView = (TextView) rootView.findViewById(R.id.forecast_detail_wind_speed_textview);
		mHumidityView = (TextView) rootView.findViewById(R.id.forecast_detail_humidity_textview);
		mPressureView = (TextView) rootView.findViewById(R.id.forecast_detail_pressure_textview);
		mMyView = (WindDirectionView) rootView.findViewById(R.id.forecast_wind_direction);
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
//		Intent intent = getActivity().getIntent();
//		if (intent != null
//				&& intent.hasExtra(DATE_KEY)
//				&& null != mLocation
//				&& !mLocation.equals(Utility
//						.getPreferredLocation(getActivity()))) {
//			getLoaderManager().restartLoader(DETAIL_LOADER, null, this);
//		}
		// No more depending on the Intent
		// Switch to use Bundle arguments
		Bundle arguments = getArguments();
		if (null != arguments
				&& arguments.containsKey(DATE_KEY)
				&& mLocation != null
				&& !mLocation.equals(Utility
						.getPreferredLocation(getActivity()))) {
			getLoaderManager().restartLoader(DETAIL_LOADER, null, this);
		}
	}

	@Override
	public Loader<Cursor> onCreateLoader(int id, Bundle args) {
		
//		Intent intent = getActivity().getIntent();
//		
//		if (null == intent || !intent.hasExtra(DATE_KEY)) {
//			return null;
//		}
		
		//String dateString = getActivity().getIntent().getStringExtra(DATE_KEY);
		
		//String dateString = intent.getStringExtra(DATE_KEY);
		
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
		
		String dateString = getArguments().getString(DATE_KEY);
		
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
			
			int weatherId = data.getInt(data.getColumnIndex(WeatherEntry.COLUMN_WEATHER_ID));
			
			int layout = Utility.getArtResourceForWeatherCondition(weatherId);
			
			//mIconView.setImageResource(R.mipmap.ic_launcher);
			mIconView.setImageResource(layout);
			 
			String dateString = Utility.getFriendlyDayString(getActivity(),
					data.getString(data.getColumnIndex(WeatherEntry.COLUMN_DATETEXT)));
			String weatherDescription = data.getString(data
					.getColumnIndex(WeatherEntry.COLUMN_SHORT_DESC));
			
			// For accessibility, add a content description to the icon field.
			mIconView.setContentDescription(weatherDescription);
 
			boolean isMetric = Utility.isMetric(getActivity());
			String high = Utility.formatTemperature(getActivity(),
			data.getDouble(data.getColumnIndex(WeatherEntry.COLUMN_MAX_TEMP)), isMetric);
			String low = Utility.formatTemperature(getActivity(),
			data.getDouble(data.getColumnIndex(WeatherEntry.COLUMN_MIN_TEMP)), isMetric);
			
			String humidity = Utility.getFormattedHumidity(getActivity(), data.getDouble(data.getColumnIndex(WeatherEntry.COLUMN_HUMIDITY)));
			
			float windSp = data.getFloat(data.getColumnIndex(WeatherEntry.COLUMN_WIND_SPEED));
			float degrees = data.getFloat(data.getColumnIndex(WeatherEntry.COLUMN_DEGREES));
			String windSpeed = Utility.getFormattedWind(getActivity(), windSp, degrees);
			
			String pressure = Utility.getFormattedPressure(getActivity(), data.getDouble(data.getColumnIndex(WeatherEntry.COLUMN_PRESSURE)));
			
			mDayView.setText(Utility.getDayName(getActivity(), dateString));
			
			//TextView dateView = (TextView) getView().findViewById(R.id.forecast_detail_date_textview);
			mDateView.setText(dateString);
			
			//TextView descView = (TextView) getView().findViewById(R.id.forecast_detail_forecast_textview);
			mForecastDescriptionView.setText(weatherDescription);
			
			//TextView highTempView = (TextView) getView().findViewById(R.id.forecast_detail_high_textview);
			mHighTempView.setText(high);
			
			//TextView lowTempView = (TextView) getView().findViewById(R.id.forecast_detail_low_textview);
			mLowTempView.setText(low);
			
			//TextView humidityView = (TextView) getView().findViewById(R.id.forecast_detail_humidity_textview);
			mWindSpeedView.setText(humidity);
			
			//TextView windSpeedView = (TextView) getView().findViewById(R.id.forecast_detail_wind_speed_textview);
			mHumidityView.setText(windSpeed);
			
			//TextView pressureView = (TextView) getView().findViewById(R.id.forecast_detail_pressure_textview);
			mPressureView.setText(pressure);
			
			mMyView.setDirection(Utility.getFormattedWindDirectionOnly(getActivity(), windSp, degrees));
			
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

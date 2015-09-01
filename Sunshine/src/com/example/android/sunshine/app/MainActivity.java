package com.example.android.sunshine.app;


import com.example.android.sunshine.sync.SunshineSyncAdapter;

import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.Fragment;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.os.Build;
import android.preference.PreferenceManager;

/**
 * Represents main activity.
 *
 */
public class MainActivity extends ActionBarActivity implements ForecastFragment.Callback {
	
	private final String LOG_TAG = MainActivity.class.getSimpleName();
	
	private boolean mTwoPane = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
//        if (savedInstanceState == null) {
//            getSupportFragmentManager().beginTransaction()
//                    .add(R.id.container, new ForecastFragment())
//                    .commit();
//        }
		if (findViewById(R.id.weather_detail_container) != null) {
	        // The detail container view will be present only in the large-screen layouts
	        // (res/layout-sw600dp). If this view is present, then the activity should be
	        // in two-pane mode.
			mTwoPane = true;
			
	        // In two-pane mode, show the detail view in this activity by
	        // adding or replacing the detail fragment using a
	        // fragment transaction.
			if (savedInstanceState == null) {
				getSupportFragmentManager()
						.beginTransaction()
						.add(R.id.weather_detail_container,
								new DetailFragment()).commit();
			}
		} else {
			mTwoPane = false;
		}
		
		ForecastFragment forecastFragment = ((ForecastFragment) getSupportFragmentManager()
				.findFragmentById(R.id.fragment_forecast));
		forecastFragment.setUseTodayLayout(!mTwoPane);
		
		//make sure we have gotten an account created and we are 
		SunshineSyncAdapter.initializeSyncAdapter(this);
    }
    
	@Override
	public void onItemSelected(String date) {
		if (mTwoPane) {
			Bundle bundleArguments = new Bundle();
			bundleArguments.putString(DetailActivity.DATE_KEY, date);

			DetailFragment detailFragment = new DetailFragment();
			detailFragment.setArguments(bundleArguments);

			getSupportFragmentManager().beginTransaction()
					.replace(R.id.weather_detail_container, detailFragment)
					.commit();
		} else {
			Intent intent = new Intent(this, DetailActivity.class).putExtra(
					DetailActivity.DATE_KEY, date);
			startActivity(intent);
		}
	}

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
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
        if (id == R.id.action_play_sound) {
        	Intent playSoundIntent = new Intent(this, PlaySoundActivity.class);
        	startActivity(playSoundIntent);
        	return true;
        }
        if (id == R.id.action_move_around) {
        	Intent moveAroundIntent = new Intent(this, MoveAroundActivity.class);
        	startActivity(moveAroundIntent);
        	return true;
        }
        return super.onOptionsItemSelected(item);
    }
    
	
//	/**
//	 * geo:latitude,longitude
//	 */
//	private void fetchPreferredLocation() {
//		SharedPreferences sharedPreferences = PreferenceManager
//				.getDefaultSharedPreferences(this);
////		String coords = sharedPreferences.getString(
////				getString(R.string.pref_location_coord),
////				getString(R.string.pref_location_coordinates));
//		String postalLocation = sharedPreferences.getString(
//				getString(R.string.pref_location_key),
//				getString(R.string.pref_location_default));
////		Uri geoLocation = Uri.parse(new StringBuilder("geo:").append(coords).append("?z=6").toString());
//		Uri geoLocation = Uri.parse("geo:0,0?").buildUpon().appendQueryParameter("q", postalLocation).build();
//		Log.i(LOG_TAG, "Default coords : " + geoLocation.toString());
//		showPreferredLocationMap(geoLocation);
//	}
//	
//	/**
//	 * Open Map application.
//	 * @param Uri geoLocation
//	 */
//	private void showPreferredLocationMap(Uri geoLocation) {
//		Intent prefLocMapIntent = new Intent(Intent.ACTION_VIEW);
//		prefLocMapIntent.setData(geoLocation);
//		if (null != prefLocMapIntent.resolveActivity(getPackageManager())) {
//			startActivity(prefLocMapIntent);
//		} else {
//			Log.i(LOG_TAG, "Error in locating " + geoLocation.toString());
//		}
//	}
}

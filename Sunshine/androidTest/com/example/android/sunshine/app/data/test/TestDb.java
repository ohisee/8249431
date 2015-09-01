/**
 * 
 */
package com.example.android.sunshine.app.data.test;

import com.example.android.sunshine.app.data.WeatherContract.LocationEntry;
import com.example.android.sunshine.app.data.WeatherContract.WeatherEntry;
import com.example.android.sunshine.app.data.WeatherDbHelper;

import android.content.ContentValues;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.test.AndroidTestCase;
import android.util.Log;

/**
 * Test Db
 *
 */
public class TestDb extends AndroidTestCase {
	
	private static final String LOG_TAG = TestDb.class.getSimpleName();
	
	public void testCreateDb() throws Throwable {
		boolean d = mContext.deleteDatabase(WeatherDbHelper.DATABASE_NAME);
		Log.i(LOG_TAG, "Delete? " + d);
		SQLiteDatabase db = new WeatherDbHelper(mContext).getWritableDatabase();
		assertEquals(true, db.isOpen());
		db.close();
	}
	
	public void testInsertDbRead() {
		// Test data
		String testCityName = "North Pole";
		String testLocationSetting = "99705";
		double testLatitude = 64.772;
		double testLongitude = -147.355;
		
		WeatherDbHelper dbHelper = new WeatherDbHelper(mContext);
		SQLiteDatabase db = dbHelper.getWritableDatabase();

		ContentValues values = new ContentValues();
		values.put(LocationEntry.COLUMN_LOCATION_SETTING, testLocationSetting);
		values.put(LocationEntry.COLUMN_CITY_NAME, testCityName);
		values.put(LocationEntry.COLUMN_COORD_LAT, testLatitude);
		values.put(LocationEntry.COLUMN_COORD_LONG, testLongitude);
		
		// Need to delete this row with test location setting
		db.delete(LocationEntry.TABLE_NAME, LocationEntry.COLUMN_LOCATION_SETTING + " = " + testLocationSetting, null);
		
		long locationRowId = db.insert(LocationEntry.TABLE_NAME, null, values);
		assertTrue(locationRowId != -1);
		Log.i(LOG_TAG, "New location row id: " + locationRowId);
		
		String[] columns = {
				 LocationEntry._ID,
				 LocationEntry.COLUMN_LOCATION_SETTING,
				 LocationEntry.COLUMN_CITY_NAME,
				 LocationEntry.COLUMN_COORD_LAT,
				 LocationEntry.COLUMN_COORD_LONG				
		};
		
		// Cursor
		Cursor cursor = db.query(LocationEntry.TABLE_NAME, // Table to Query
				columns, null, // Columns for the "where" clause
				null, // Values for the "where" clause
				null, // columns to group by
				null, // columns to filter by row groups
				null // sort order
				);
		
		// If possible, move to the first row of the query results.
		if (cursor.moveToFirst()) {
			// Get the value in each column by finding the appropriate column
			// index.
			int locationIndex = cursor.getColumnIndex(LocationEntry.COLUMN_LOCATION_SETTING);
			String location = cursor.getString(locationIndex);
			int nameIndex = cursor.getColumnIndex(LocationEntry.COLUMN_CITY_NAME);
			String name = cursor.getString(nameIndex);
			int latIndex = cursor.getColumnIndex(LocationEntry.COLUMN_COORD_LAT);
			double latitude = cursor.getDouble(latIndex);
			int longIndex = cursor.getColumnIndex(LocationEntry.COLUMN_COORD_LONG);
			double longitude = cursor.getDouble(longIndex);
			// Hooray, data was returned! Assert that it's the right data, and
			// that the database
			// creation code is working as intended.
			// Then take a break. We both know that wasn't easy.
			assertEquals(testCityName, name);
			assertEquals(testLocationSetting, location);
			assertEquals(testLatitude, latitude);
			assertEquals(testLongitude, longitude);
			
			// Fantastic. Now that we have a location, add some weather!
			ContentValues weatherValues = new ContentValues();
			weatherValues.put(WeatherEntry.COLUMN_LOC_KEY, locationRowId);
			weatherValues.put(WeatherEntry.COLUMN_DATETEXT, "20141205");
			weatherValues.put(WeatherEntry.COLUMN_DEGREES, 1.1);
			weatherValues.put(WeatherEntry.COLUMN_HUMIDITY, 1.2);
			weatherValues.put(WeatherEntry.COLUMN_PRESSURE, 1.3);
			weatherValues.put(WeatherEntry.COLUMN_MAX_TEMP, 75);
			weatherValues.put(WeatherEntry.COLUMN_MIN_TEMP, 65);
			weatherValues.put(WeatherEntry.COLUMN_SHORT_DESC, "Asteroids");
			weatherValues.put(WeatherEntry.COLUMN_WIND_SPEED, 5.5);
			weatherValues.put(WeatherEntry.COLUMN_WEATHER_ID, 321);
			
			long weatherRowId = db.insert(WeatherEntry.TABLE_NAME, null, weatherValues);
			assertTrue(weatherRowId != -1);
			Log.i(LOG_TAG, "New weather row id: " + weatherRowId);
			
			String[] weatherColumns = {
					WeatherEntry._ID,
					WeatherEntry.COLUMN_LOC_KEY,
					WeatherEntry.COLUMN_DATETEXT,
					WeatherEntry.COLUMN_DEGREES,
					WeatherEntry.COLUMN_HUMIDITY,
					WeatherEntry.COLUMN_PRESSURE,
					WeatherEntry.COLUMN_MAX_TEMP,
					WeatherEntry.COLUMN_MIN_TEMP,
					WeatherEntry.COLUMN_SHORT_DESC,
					WeatherEntry.COLUMN_WIND_SPEED,
					WeatherEntry.COLUMN_WEATHER_ID			
			};
			
			// Cursor
			Cursor wcursor = db.query(WeatherEntry.TABLE_NAME, // Table to Query
					weatherColumns, null, // Columns for the "where" clause
					null, // Values for the "where" clause
					null, // columns to group by
					null, // columns to filter by row groups
					null // sort order
					);
			
			if (wcursor.moveToFirst()) {
				// Read date
				int dateIndex = wcursor.getColumnIndex(WeatherEntry.COLUMN_DATETEXT);
				String date = wcursor.getString(dateIndex);
				assertEquals(date, "20141205");
			} else {
				fail("No weather values returned");
			}
			
			wcursor.close();
			 
			dbHelper.close();
			
		} else {
			// That's weird, it works on MY machine...
			fail("No values returned :(");
		}
		
		db.close();
		cursor.close();
	}
}

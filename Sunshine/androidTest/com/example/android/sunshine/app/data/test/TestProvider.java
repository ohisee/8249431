/**
 * 
 */
package com.example.android.sunshine.app.data.test;

import java.io.File;
import java.util.Map.Entry;
import java.util.Set;

import android.content.ContentUris;
import android.content.ContentValues;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.net.Uri;
import android.test.AndroidTestCase;
import android.util.Log;

import com.example.android.sunshine.app.data.WeatherContract;
import com.example.android.sunshine.app.data.WeatherContract.LocationEntry;
import com.example.android.sunshine.app.data.WeatherContract.WeatherEntry;
import com.example.android.sunshine.app.data.WeatherDbHelper;

/**
 * This is test provider.
 *
 */
public class TestProvider extends AndroidTestCase {
	
	private static final String LOG_TAG = TestProvider.class.getSimpleName();
	
	public void testDeleteDb() throws Throwable {
		boolean d = mContext.deleteDatabase(WeatherDbHelper.DATABASE_NAME);
		Log.i(LOG_TAG, "Delete? " + d);
//		SQLiteDatabase db = new WeatherDbHelper(mContext).getWritableDatabase();
//		assertEquals(true, db.isOpen());
//		db.close();
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
		//db.delete(LocationEntry.TABLE_NAME, LocationEntry.COLUMN_LOCATION_SETTING + " = " + testLocationSetting, null);
		
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
			
			assertTrue(wcursor.moveToFirst());
			Set<Entry<String, Object>> expectedValues = weatherValues.valueSet();
			for (Entry<String, Object> expectedValue : expectedValues) {
				String columnName = expectedValue.getKey();
				int index = wcursor.getColumnIndex(columnName);
				assertTrue(index != -1);
				assertEquals(wcursor.getString(index), expectedValue.getValue().toString());
				assertEquals(wcursor.getString(index), weatherValues.getAsString(expectedValue.getKey()));
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
	
	public void testGetType() {
		// content://com.example.android.sunshine.app/weather/
		String type = mContext.getContentResolver().getType(
				WeatherEntry.CONTENT_URI);
		
		// vnd.android.cursor.dir/com.example.android.sunshine.app/weather
		assertEquals(WeatherEntry.CONTENT_TYPE, type);
		
		String testLocation = "94074";
		// content://com.example.android.sunshine.app/weather/94074
		type = mContext.getContentResolver().getType(
				WeatherEntry.buildWeatherLocation(testLocation));
		
		// vnd.android.cursor.dir/com.example.android.sunshine.app/weather
		assertEquals(WeatherEntry.CONTENT_TYPE, type);
		
		String testDate = "20140612";
		// content://com.example.android.sunshine.app/weather/94074/20140612
		type = mContext.getContentResolver().getType(
				WeatherEntry.buildWeatherLocationWithDate(testLocation,
						testDate));
		
		// vnd.android.cursor.item/com.example.android.sunshine.app/weather
		assertEquals(WeatherEntry.CONTENT_ITEM_TYPE, type);
		
		// content://com.example.android.sunshine.app/location/
		type = mContext.getContentResolver().getType(LocationEntry.CONTENT_URI);
		
		// vnd.android.cursor.dir/com.example.android.sunshine.app/location
		assertEquals(LocationEntry.CONTENT_TYPE, type);
		
		// content://com.example.android.sunshine.app/location/1
		type = mContext.getContentResolver().getType(
				LocationEntry.buildLocationUri(1L));
		
		// vnd.android.cursor.item/com.example.android.sunshine.app/location
		assertEquals(LocationEntry.CONTENT_ITEM_TYPE, type);
	}
	
	private static String TEST_CITY_NAME = "North Pole";
	private static String TEST_LOCATION_SETTING = "99705";
	private static String TEST_COLUMN_DATETEXT = "20141205";
	private static double TEST_LATITUDE = 64.772;
	private static double TEST_LONGITUDE = -147.355;
	private static String TEST_UPDATE_CIY_NAME = "Santa's Village";
	
	public void testInsertReadProvider() {
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
		
		// Use content provider's insert - insert location data
		Uri returnedUri = mContext.getContentResolver().insert(LocationEntry.CONTENT_URI, values);
		long locationRowId = ContentUris.parseId(returnedUri);
		Log.i(LOG_TAG, "New location row id: " + locationRowId);
		
		String[] columns = {
				 LocationEntry._ID,
				 LocationEntry.COLUMN_LOCATION_SETTING,
				 LocationEntry.COLUMN_CITY_NAME,
				 LocationEntry.COLUMN_COORD_LAT,
				 LocationEntry.COLUMN_COORD_LONG				
		};
		
		// Cursor
		// Location cursor created from content provider
		Cursor cursor = mContext.getContentResolver().query(
				LocationEntry.CONTENT_URI, columns, null, null, null);

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
			
			// Use content provider's insert - insert weather data
			Uri returnUri = mContext.getContentResolver().insert(WeatherEntry.CONTENT_URI, weatherValues);
			long weatherRowId = ContentUris.parseId(returnUri);
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
			// Create a cursor from content provider
			Cursor wcursor = mContext.getContentResolver().query(
					WeatherEntry.CONTENT_URI, weatherColumns, null, null, null);
			
			assertTrue(wcursor.moveToFirst());
			Set<Entry<String, Object>> expectedValues = weatherValues.valueSet();
			for (Entry<String, Object> expectedValue : expectedValues) {
				String columnName = expectedValue.getKey();
				int index = wcursor.getColumnIndex(columnName);
				assertTrue(index != -1);
				assertEquals(wcursor.getString(index), expectedValue.getValue().toString());
				assertEquals(wcursor.getString(index), weatherValues.getAsString(expectedValue.getKey()));
			}
			wcursor.close();

			// Test join
			Uri uri = WeatherEntry.buildWeatherLocation(TEST_LOCATION_SETTING);
			Log.i(LOG_TAG, "URI formed is : " + uri);
			// leaving "columns" null just returns all the columns.
			// cols for "where" clause
			// values for "where" clause
			// sort order
			Cursor weatherJoinCursor = mContext.getContentResolver().query(uri,
					null, null, null, null);
			assertTrue(weatherJoinCursor.moveToFirst());
			for (Entry<String, Object> expectedValue : expectedValues) {
				String columnName = expectedValue.getKey();
				int index = weatherJoinCursor.getColumnIndex(columnName);
				assertTrue(index != -1);
				assertEquals(weatherJoinCursor.getString(index), expectedValue.getValue().toString());
				assertEquals(weatherJoinCursor.getString(index), weatherValues.getAsString(expectedValue.getKey()));
			}
			weatherJoinCursor.close();
			
			// Test join location setting and start date
			uri = WeatherEntry.buildWeatherLocationWithStartDate(
					TEST_LOCATION_SETTING, TEST_COLUMN_DATETEXT);
			Log.i(LOG_TAG, "URI using start date formed is : " + uri);
			// leaving "columns" null just returns all the columns.
			Cursor weatherJoinDateCursor = mContext.getContentResolver().query(
					uri, null, null, null, null);
			assertTrue(weatherJoinDateCursor.moveToFirst());
			for (Entry<String, Object> expectedValue : expectedValues) {
				String columnName = expectedValue.getKey();
				int index = weatherJoinDateCursor.getColumnIndex(columnName);
				assertTrue(index != -1);
				assertEquals(weatherJoinDateCursor.getString(index), expectedValue.getValue().toString());
				assertEquals(weatherJoinDateCursor.getString(index), weatherValues.getAsString(expectedValue.getKey()));
			}
			weatherJoinDateCursor.close();
			
			// Test join location setting and a date
			uri = WeatherEntry.buildWeatherLocationWithDate(TEST_LOCATION_SETTING, TEST_COLUMN_DATETEXT);
			Log.i(LOG_TAG, "URI using date formed is : " + uri);
			Cursor weatherJoinLocAndDate = mContext.getContentResolver().query(uri, null, null, null, null);
			assertTrue(weatherJoinLocAndDate.moveToFirst());
			for (Entry<String, Object> expectedValue : expectedValues) {
				String columnName = expectedValue.getKey();
				int index = weatherJoinLocAndDate.getColumnIndex(columnName);
				assertTrue(index != -1);
				assertEquals(weatherJoinLocAndDate.getString(index), expectedValue.getValue().toString());
				assertEquals(weatherJoinLocAndDate.getString(index), weatherValues.getAsString(expectedValue.getKey()));				
			}
			weatherJoinLocAndDate.close();
			
			
		} else {
			// That's weird, it works on MY machine...
			fail("No values returned :(");
		}
		
		cursor.close();
		dbHelper.close();
		db.close();
	}
	

	public void insertLocationByContentProviderForRead() {
		Log.i(LOG_TAG, "Calling Insert Location By Content Provider For Read");

		ContentValues values = new ContentValues();
		values.put(LocationEntry.COLUMN_LOCATION_SETTING, TEST_LOCATION_SETTING);
		values.put(LocationEntry.COLUMN_CITY_NAME, TEST_CITY_NAME);
		values.put(LocationEntry.COLUMN_COORD_LAT, TEST_LATITUDE);
		values.put(LocationEntry.COLUMN_COORD_LONG, TEST_LONGITUDE);
		
		// Use content provider's insert - insert location data
		Uri returnedUri = mContext.getContentResolver().insert(LocationEntry.CONTENT_URI, values);
		long locationRowId = ContentUris.parseId(returnedUri);
		Log.i(LOG_TAG, "New location row id: " + locationRowId);
		
		String[] columns = {
				 LocationEntry._ID,
				 LocationEntry.COLUMN_LOCATION_SETTING,
				 LocationEntry.COLUMN_CITY_NAME,
				 LocationEntry.COLUMN_COORD_LAT,
				 LocationEntry.COLUMN_COORD_LONG				
		};
		
		// Cursor Location cursor created from content provider
		Cursor cursor = mContext.getContentResolver().query(
				LocationEntry.CONTENT_URI, columns, null, null, null);
		
		assertTrue(cursor.moveToFirst());
		
		cursor.close();
	}
	
	public void insertLocationAndWeatherByContentProviderForRead() {
		Log.i(LOG_TAG, "Calling Insert Location and Weather By Content Provider For Read");

		ContentValues values = new ContentValues();
		values.put(LocationEntry.COLUMN_LOCATION_SETTING, TEST_LOCATION_SETTING);
		values.put(LocationEntry.COLUMN_CITY_NAME, TEST_CITY_NAME);
		values.put(LocationEntry.COLUMN_COORD_LAT, TEST_LATITUDE);
		values.put(LocationEntry.COLUMN_COORD_LONG, TEST_LONGITUDE);
		
		// Use content provider's insert - insert location data
		Uri returnedUri = mContext.getContentResolver().insert(LocationEntry.CONTENT_URI, values);
		long locationRowId = ContentUris.parseId(returnedUri);
		Log.i(LOG_TAG, "New location row id: " + locationRowId);
		
		String[] columns = {
				 LocationEntry._ID,
				 LocationEntry.COLUMN_LOCATION_SETTING,
				 LocationEntry.COLUMN_CITY_NAME,
				 LocationEntry.COLUMN_COORD_LAT,
				 LocationEntry.COLUMN_COORD_LONG				
		};
		
		// Cursor Location cursor created from content provider
		Cursor cursor = mContext.getContentResolver().query(
				LocationEntry.CONTENT_URI, columns, null, null, null);

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
			assertEquals(TEST_CITY_NAME, name);
			assertEquals(TEST_LOCATION_SETTING, location);
			assertEquals(TEST_LATITUDE, latitude);
			assertEquals(TEST_LONGITUDE, longitude);
			
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
			
			// Use content provider's insert - insert weather data
			Uri returnUri = mContext.getContentResolver().insert(WeatherEntry.CONTENT_URI, weatherValues);
			long weatherRowId = ContentUris.parseId(returnUri);
			Log.i(LOG_TAG, "New weather row id: " + weatherRowId);
		}
		
		cursor.close();
	}
	
	public void testReadLocation() {
		Log.i(LOG_TAG, "Calling Test Read Location");
		
		insertLocationByContentProviderForRead();
		
		String[] columns = {
				 LocationEntry._ID,
				 LocationEntry.COLUMN_LOCATION_SETTING,
				 LocationEntry.COLUMN_CITY_NAME,
				 LocationEntry.COLUMN_COORD_LAT,
				 LocationEntry.COLUMN_COORD_LONG				
		};
		 
		Cursor lcursor = mContext.getContentResolver().query(LocationEntry.CONTENT_URI, columns, null, null, null);
		assertTrue(lcursor.moveToFirst());
		
		long _id = lcursor.getLong(lcursor.getColumnIndex(LocationEntry._ID));
		Log.i(LOG_TAG, "Lookup location Id : " + _id);
		Cursor lidcursor = mContext.getContentResolver().query(
				LocationEntry.buildLocationUri(_id), columns,
				null, null, null);
		assertTrue(lidcursor.moveToFirst());
		
		lcursor.close();
		lidcursor.close();
	}
	
	
	public void testUpdateLocation() {
		
		Log.i(LOG_TAG, "Calling Test Update Location");
		
		ContentValues values = new ContentValues();
		values.put(LocationEntry.COLUMN_LOCATION_SETTING, TEST_LOCATION_SETTING);
		values.put(LocationEntry.COLUMN_CITY_NAME, TEST_CITY_NAME);
		values.put(LocationEntry.COLUMN_COORD_LAT, TEST_LATITUDE);
		values.put(LocationEntry.COLUMN_COORD_LONG, TEST_LONGITUDE);
		
		// Use content provider's insert - insert location data
		Uri returnedUri = mContext.getContentResolver().insert(LocationEntry.CONTENT_URI, values);
		long locationRowId = ContentUris.parseId(returnedUri);
		Log.i(LOG_TAG, "New location row id: " + locationRowId);
		
		ContentValues updatedLocationValues = new ContentValues(values);
		updatedLocationValues.put(LocationEntry._ID, locationRowId);
		updatedLocationValues.put(LocationEntry.COLUMN_CITY_NAME, TEST_UPDATE_CIY_NAME);
		
		int count = mContext.getContentResolver().update(
				LocationEntry.CONTENT_URI, updatedLocationValues,
				LocationEntry._ID + "= ?",
				new String[] { Long.toString(locationRowId) });
		
		assertEquals(1, count);
		
		// Validate the cursor
		String[] columns = {
				 LocationEntry._ID,
				 LocationEntry.COLUMN_LOCATION_SETTING,
				 LocationEntry.COLUMN_CITY_NAME,
				 LocationEntry.COLUMN_COORD_LAT,
				 LocationEntry.COLUMN_COORD_LONG				
		};
		
		// Cursor Location cursor created from content provider
		Cursor cursor = mContext.getContentResolver().query(
				LocationEntry.CONTENT_URI, columns, null, null, null);
		
		assertTrue(cursor.moveToFirst());
		
		Set<Entry<String, Object>> expectedValues = updatedLocationValues.valueSet();
		for (Entry<String, Object> expectedValue : expectedValues) {
			String columnName = expectedValue.getKey();
			int index = cursor.getColumnIndex(columnName);
			assertTrue(index != -1);
			assertEquals(cursor.getString(index), expectedValue.getValue().toString());
			assertEquals(cursor.getString(index), updatedLocationValues.getAsString(expectedValue.getKey()));
		}
		cursor.close();
	}
	
	// Remove rows
	public void deleteAllRecords() {
		Log.i(LOG_TAG, "Calling Delete All Records");
		mContext.getContentResolver().delete(WeatherEntry.CONTENT_URI, null, null);
		mContext.getContentResolver().delete(LocationEntry.CONTENT_URI, null, null);
		
		Cursor cursor = mContext.getContentResolver().query(
				WeatherEntry.CONTENT_URI, null, null, null, null);
		assertEquals(0, cursor.getCount());
		cursor.close();

		cursor = mContext.getContentResolver().query(LocationEntry.CONTENT_URI,
				null, null, null, null);
		assertEquals(0, cursor.getCount());
		cursor.close();
	}

	// Since we want each test to start with a clean slate, run deleteAllRecords
	// in setUp (called by the test runner before each test).
	public void setUp() {
		Log.i(LOG_TAG, "Calling Set Up test case");
		File dbFile = mContext.getDatabasePath(WeatherDbHelper.DATABASE_NAME);
		if (dbFile.exists()) {
			deleteAllRecords();
		}
	}
}
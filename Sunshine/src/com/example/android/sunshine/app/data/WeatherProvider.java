/**
 * 
 */
package com.example.android.sunshine.app.data;

import android.content.ContentProvider;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.UriMatcher;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteQueryBuilder;
import android.net.Uri;
import android.util.Log;

/**
 * This is weather provider.
 * {@link ContentProvider}
 *
 */
public class WeatherProvider extends ContentProvider {
	
	private static final String LOG_TAG = WeatherProvider.class.getSimpleName();
	
	private static final int WEATHER = 100;
	private static final int WEATHER_WITH_LOCATION = 101;
	private static final int WEATHER_WITH_LOCATION_AND_DATE = 102;
	private static final int LOCATION = 300;
	private static final int LOCATION_ID = 301;
	
	private WeatherDbHelper mOpenHelper;
	
	private static final UriMatcher uriMatcher = buildUriMatcher();
	
	private static UriMatcher buildUriMatcher() {
		final String AUTHORITY = WeatherContract.CONTENT_AUTHORITY;
		final String PATH_weather = WeatherContract.PATH_WEATHER;
		final String PATH_location = WeatherContract.PATH_LOCATION;
		UriMatcher uriMatcher = new UriMatcher(UriMatcher.NO_MATCH);
		uriMatcher.addURI(AUTHORITY, PATH_weather, WEATHER);
		uriMatcher.addURI(AUTHORITY, PATH_weather + "/*", WEATHER_WITH_LOCATION);
		uriMatcher.addURI(AUTHORITY, PATH_weather + "/*/*", WEATHER_WITH_LOCATION_AND_DATE);
		uriMatcher.addURI(AUTHORITY, PATH_location, LOCATION);
		uriMatcher.addURI(AUTHORITY, PATH_location + "/#", LOCATION_ID);
		return uriMatcher;
	}
	
	private static final SQLiteQueryBuilder sWeatherByLocationSettingQueryBuilder;
	
	static {
		sWeatherByLocationSettingQueryBuilder = new SQLiteQueryBuilder();
		sWeatherByLocationSettingQueryBuilder
				.setTables(WeatherContract.WeatherEntry.TABLE_NAME
						+ " INNER JOIN "
						+ WeatherContract.LocationEntry.TABLE_NAME + " ON "
						+ WeatherContract.WeatherEntry.TABLE_NAME + "."
						+ WeatherContract.WeatherEntry.COLUMN_LOC_KEY + " = "
						+ WeatherContract.LocationEntry.TABLE_NAME + "."
						+ WeatherContract.LocationEntry._ID);
	}
	
	// Define query
	private static final String sLocationSettingSelection = WeatherContract.LocationEntry.TABLE_NAME
			+ "."
			+ WeatherContract.LocationEntry.COLUMN_LOCATION_SETTING
			+ " = ? ";	
	
	// Second selection on greater than Date
	private static final String sLocationSettingWithStartDateSelection = WeatherContract.LocationEntry.TABLE_NAME
			+ "."
			+ WeatherContract.LocationEntry.COLUMN_LOCATION_SETTING
			+ " = ? AND "
			+ WeatherContract.WeatherEntry.COLUMN_DATETEXT
			+ " >= ?";
	
	// Third selection on Date
	private static final String sLocationSettingWithDateSelection = WeatherContract.LocationEntry.TABLE_NAME
			+ "."
			+ WeatherContract.LocationEntry.COLUMN_LOCATION_SETTING
			+ " = ? AND "
			+ WeatherContract.WeatherEntry.COLUMN_DATETEXT
			+ " = ?";
	

	// Location setting join or no join
	private Cursor getWeatherByLocationSetting(Uri uri, String[] projection, String sortOrder) {
		String locationSetting = WeatherContract.WeatherEntry.getLocationSettingFromUri(uri);
		String startDate = WeatherContract.WeatherEntry.getStartDateFromUri(uri);
		
		String[] selectionArgs;
		String selection;
		
		if (null == startDate) {
			selection = sLocationSettingSelection;
			selectionArgs = new String[] {locationSetting};
		} else {
			selectionArgs = new String[] {locationSetting, startDate};
			selection = sLocationSettingWithStartDateSelection;
		}
		
		Log.i(LOG_TAG, "selection is " + selection);
		
		return sWeatherByLocationSettingQueryBuilder.query(
				mOpenHelper.getReadableDatabase(), projection, selection,
				selectionArgs, null, null, sortOrder);
	}
	
	// Location setting join or no join
	private Cursor getWeatherByLocationSettingAndDate(Uri uri, String[] projection, String sortOrder) {
		String locationSetting = WeatherContract.WeatherEntry.getLocationSettingFromUri(uri);
		String startDate = null;
		if (uri.getPathSegments().size() >= 2) {
			startDate = WeatherContract.WeatherEntry.getDateFromUri(uri);
		}
		
		String[] selectionArgs;
		String selection;
		
		if (null == startDate) {
			selection = sLocationSettingSelection;
			selectionArgs = new String[] {locationSetting};
		} else {
			selectionArgs = new String[] {locationSetting, startDate};
			selection = sLocationSettingWithDateSelection;
		}
		
		Log.i(LOG_TAG, "selection is " + selection);
		
		return sWeatherByLocationSettingQueryBuilder.query(
				mOpenHelper.getReadableDatabase(), projection, selection,
				selectionArgs, null, null, sortOrder);
	}

	@Override
	public int delete(Uri uri, String selection, String[] selectionArgs) {
		final SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		final int match = uriMatcher.match(uri);
		int row = 0;
		
		switch(match) {
			case WEATHER: {
				row = db.delete(WeatherContract.WeatherEntry.TABLE_NAME, selection, selectionArgs);
				break;
			}
			case LOCATION: {
				row = db.delete(WeatherContract.LocationEntry.TABLE_NAME, selection, selectionArgs);
				break;
			}
			default:
				throw new UnsupportedOperationException("Unknown uri: " + uri);
		}

		if (null == selection || 0 != row) {
			Log.i(LOG_TAG, "Deleted " + row + " row(s).");
			// Notify any (content) observers
			getContext().getContentResolver().notifyChange(uri, null);
		}
		
		return row;
	}

	@Override
	public String getType(Uri uri) {
		final int match = uriMatcher.match(uri);
		switch (match) {
			case WEATHER_WITH_LOCATION_AND_DATE:
				return WeatherContract.WeatherEntry.CONTENT_ITEM_TYPE;
			case WEATHER_WITH_LOCATION:
				return WeatherContract.WeatherEntry.CONTENT_TYPE;
			case WEATHER:
				return WeatherContract.WeatherEntry.CONTENT_TYPE;
			case LOCATION:
				return WeatherContract.LocationEntry.CONTENT_TYPE;
			case LOCATION_ID:
				return WeatherContract.LocationEntry.CONTENT_ITEM_TYPE;
			default:
				throw new UnsupportedOperationException("Unknown uri: " + uri);
		}
	}

	@Override
	public Uri insert(Uri uri, ContentValues values) {
		final SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		final int match = uriMatcher.match(uri);
		Uri returnUri;
		
		switch(match) {
			case WEATHER: {
				long _id = db.insert(WeatherContract.WeatherEntry.TABLE_NAME, null, values);
				if (_id > 0) {
					returnUri = WeatherContract.WeatherEntry.buildWeatherUri(_id);
				} else {
					throw new android.database.SQLException("Failed to insert row into " + uri);
				}
				break;
			}
			case LOCATION: {
				long _id = db.insert(WeatherContract.LocationEntry.TABLE_NAME, null, values);
				if (_id > 0) {
					returnUri = WeatherContract.LocationEntry.buildLocationUri(_id);
				} else {
					throw new android.database.SQLException("Failed to insert row into " + uri);
				}
				break;
			}
			default:
				throw new UnsupportedOperationException("Unknown uri: " + uri);
		}
		
		// Notify any (content) observers
		getContext().getContentResolver().notifyChange(returnUri, null);
		
		return returnUri;
	}

	/** 
	 * To initialize.
	 */
	@Override
	public boolean onCreate() {
		mOpenHelper = new WeatherDbHelper(getContext());
		return true;
	}

	@Override
	public Cursor query(Uri uri, String[] projection, String selection,
			String[] selectionArgs, String sortOrder) {
		
		Cursor retCursor;
		switch (uriMatcher.match(uri)) {
			// "weather/*/*"
			case WEATHER_WITH_LOCATION_AND_DATE: {
				Log.i(LOG_TAG, "Query type is WEATHER_WITH_LOCATION_AND_DATE");
				retCursor = getWeatherByLocationSettingAndDate(uri, projection, sortOrder);
				break;
			}
			// "weather/*"
			case WEATHER_WITH_LOCATION: {
				Log.i(LOG_TAG, "Query type is WEATHER_WITH_LOCATION");
				retCursor = getWeatherByLocationSetting(uri, projection, sortOrder);
				break;
			}
			// "weather"
			case WEATHER: {
				retCursor = mOpenHelper.getReadableDatabase().query(
						WeatherContract.WeatherEntry.TABLE_NAME, projection,
						selection, selectionArgs, null, null, sortOrder);
				break;
			}
			// "location/*"
			case LOCATION_ID: {
				long _id = ContentUris.parseId(uri);
				retCursor = mOpenHelper.getReadableDatabase().query(
						WeatherContract.LocationEntry.TABLE_NAME, projection,
						WeatherContract.LocationEntry._ID + " = '" + _id + "'", null, null, null, sortOrder);
				break;
			}
			// "location"
			case LOCATION: {
				retCursor = mOpenHelper.getReadableDatabase().query(
						WeatherContract.LocationEntry.TABLE_NAME, projection,
						selection, selectionArgs, null, null, sortOrder);
				break;
			}
	
			default:
				throw new UnsupportedOperationException("Unknown uri: " + uri);
		}
		
		// Register Uri in observer
		retCursor.setNotificationUri(getContext().getContentResolver(), uri);
		return retCursor;
	}

	@Override
	public int update(Uri uri, ContentValues values, String selection,
			String[] selectionArgs) {
		
		final SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		final int match = uriMatcher.match(uri);
		int row = 0;
		
		switch(match) {
			case WEATHER: {
				row = db.update(WeatherContract.WeatherEntry.TABLE_NAME, values, selection, selectionArgs);
				break;
			}
			case LOCATION: {
				row = db.update(WeatherContract.LocationEntry.TABLE_NAME, values, selection, selectionArgs);
				break;
			}
			default:
				throw new UnsupportedOperationException("Unknown uri: " + uri);
		}
		
		if (0 != row) {
			// Notify any (content) observers
			getContext().getContentResolver().notifyChange(uri, null);
		}
		
		return row;
	}

	/**
	 * Use transaction for bulk insert.
	 * @param Uri uri
	 * @param ContentValues[] values
	 */
	@Override
	public int bulkInsert(Uri uri, ContentValues[] values) {
		final SQLiteDatabase db = mOpenHelper.getWritableDatabase();
		final int match = uriMatcher.match(uri);
		switch (match) {
			case WEATHER: {
				db.beginTransaction();
				int returnCount = 0;
				try {
					for (ContentValues value : values) {
						long _id = db.insert(WeatherContract.WeatherEntry.TABLE_NAME, null, value);
						if (_id != -1) {
							returnCount++;
						}
					}
					db.setTransactionSuccessful();
				} finally {
					db.endTransaction();
				}
				getContext().getContentResolver().notifyChange(uri, null);
				return returnCount;
			}
			default:
				return super.bulkInsert(uri, values);
		}
	}
	
}
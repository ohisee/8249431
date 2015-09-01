/**
 * 
 */
package com.example.android.sunshine.app.data;

import android.content.Context;
import android.database.DatabaseErrorHandler;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.database.sqlite.SQLiteOpenHelper;

import com.example.android.sunshine.app.data.WeatherContract.LocationEntry;
import com.example.android.sunshine.app.data.WeatherContract.WeatherEntry;

/**
 * Weather DB helper.
 *
 */
public class WeatherDbHelper extends SQLiteOpenHelper {
	
	private static final int DATABASE_VERSION = 1;
	public static final String DATABASE_NAME = "weather.db";

	/**
	 * Constructor
	 * @param context
	 */
	public WeatherDbHelper(Context context) {
		super(context, DATABASE_NAME, null, DATABASE_VERSION);
	}

	/**
	 * ON CREATE
	 */
	@Override
	public void onCreate(SQLiteDatabase sqLiteDatabase) {
		
		final String SQL_CREATE_WEATHER_TABLE = new StringBuilder(
				"CREATE TABLE ")
				.append(WeatherEntry.TABLE_NAME)
				.append(" (")
				.append(WeatherEntry._ID)
				.append(" INTEGER PRIMARY KEY AUTOINCREMENT,")
				.append(WeatherEntry.COLUMN_LOC_KEY)
				.append(" INTEGER NOT NULL, ")
				.append(WeatherEntry.COLUMN_DATETEXT)
				.append(" TEXT NOT NULL, ")
				.append(WeatherEntry.COLUMN_SHORT_DESC)
				.append(" TEXT NOT NULL, ")
				.append(WeatherEntry.COLUMN_WEATHER_ID)
				.append(" INTEGER NOT NULL,")
				.append(WeatherEntry.COLUMN_MIN_TEMP)
				.append(" REAL NOT NULL, ")
				.append(WeatherEntry.COLUMN_MAX_TEMP)
				.append(" REAL NOT NULL, ")
				.append(WeatherEntry.COLUMN_HUMIDITY)
				.append(" REAL NOT NULL, ")
				.append(WeatherEntry.COLUMN_PRESSURE)
				.append(" REAL NOT NULL, ")
				.append(WeatherEntry.COLUMN_WIND_SPEED)
				.append(" REAL NOT NULL, ")
				.append(WeatherEntry.COLUMN_DEGREES)
				.append(" REAL NOT NULL, ")

				// Set up the location column as a foreign key to location
				// table.
				.append(" FOREIGN KEY (").append(WeatherEntry.COLUMN_LOC_KEY)
				.append(") REFERENCES ")
				.append(LocationEntry.TABLE_NAME)
				.append(" (")
				.append(LocationEntry._ID)
				.append("), ")

				// To assure the application have just one weather entry per day
				// per location, it's created a UNIQUE constraint with REPLACE
				// strategy
				.append(" UNIQUE (").append(WeatherEntry.COLUMN_DATETEXT)
				.append(", ").append(WeatherEntry.COLUMN_LOC_KEY)
				.append(") ON CONFLICT REPLACE);").toString();
		
		final String SQL_CREATE_LOCATION_TABLE = new StringBuilder(
				"CREATE TABLE ").append(LocationEntry.TABLE_NAME).append(" (")
				.append(LocationEntry._ID)
				.append(" INTEGER PRIMARY KEY, ")
				.append(LocationEntry.COLUMN_LOCATION_SETTING)
				.append(" TEXT UNIQUE NOT NULL, ")
				.append(LocationEntry.COLUMN_CITY_NAME)
				.append(" TEXT NOT NULL, ")
				.append(LocationEntry.COLUMN_COORD_LAT)
				.append(" REAL NOT NULL, ")
				.append(LocationEntry.COLUMN_COORD_LONG)
				.append(" REAL NOT NULL, ").append(" UNIQUE (")
				.append(LocationEntry.COLUMN_LOCATION_SETTING)
				.append(") ON CONFLICT IGNORE").append(");").toString();
		
		sqLiteDatabase.execSQL(SQL_CREATE_LOCATION_TABLE);
		sqLiteDatabase.execSQL(SQL_CREATE_WEATHER_TABLE);
	}

	@Override
	public void onUpgrade(SQLiteDatabase sqLiteDatabase, int oldVersion, int newVersion) {
		sqLiteDatabase.execSQL("DROP TABLE IF EXISTS " + LocationEntry.TABLE_NAME);
		sqLiteDatabase.execSQL("DROP TABLE IF EXISTS " + WeatherEntry.TABLE_NAME);
		onCreate(sqLiteDatabase);
	}

}

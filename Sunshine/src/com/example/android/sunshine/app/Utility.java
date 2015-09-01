/**
 * 
 */
package com.example.android.sunshine.app;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;

import com.example.android.sunshine.app.data.WeatherContract;

/**
 * This is a utility.
 *
 */
public class Utility {
	
	public static final String DATE_FORMAT = "yyyyMMdd";
	
	public static final String UNKNOWN_WIND_DIRECTION = "unknown";
	
	private Utility() {}
	
	/**
	 * @param Context context
	 * @return a preferred location in String
	 */
	public static String getPreferredLocation(Context context) {
		SharedPreferences sharedPreferences = PreferenceManager
				.getDefaultSharedPreferences(context);
		String preferredLocation = sharedPreferences.getString(
				context.getString(R.string.pref_location_key),
				context.getString(R.string.pref_location_default));
		return preferredLocation;
	}
	
	/**
	 * @param Context context
	 * @return true if temperature is in metric
	 */
	public static boolean isMetric(Context context) {
		SharedPreferences prefs = PreferenceManager
				.getDefaultSharedPreferences(context);
		return prefs.getString(context.getString(R.string.pref_temperature_unit_key),
				context.getString(R.string.pref_temperature_default_metric)).equals(
				context.getString(R.string.pref_temperature_default_metric));
	}
	
	/**
	 * @param double temperature
	 * @param boolean isMetric
	 * @return String of formated temperature
	 */
	public static String formatTemperature(double temperature, boolean isMetric) {
		double temp;
		if (!isMetric) {
			temp = 9 * temperature / 5 + 32;
		} else {
			temp = temperature;
		}
		return String.format(Locale.getDefault(), "%.0f", temp);
	}
	
	/**
	 * @param Context context
	 * @param double temperature
	 * @param boolean isMetric
	 * @return String of formated temperature
	 */
	public static String formatTemperature(Context context, double temperature, boolean isMetric) {
		double temp;
		if (!isMetric) {
			temp = 9 * temperature / 5 + 32;
		} else {
			temp = temperature;
		}
		return context.getString(R.string.format_temperature, temp);
	}
	
	/**
	 * @param String dateString
	 * @return string of formated date
	 */
	public static String formatDate(String dateString) {
		Date date = WeatherContract.getDateFromDb(dateString);
		return DateFormat.getDateInstance().format(date);
	}
	
	/**
	 * Helper method to convert the database representation of the date into
	 * something to display to users. As classy and polished a user experience
	 * as "20140102" is, we can do better.
	 * 
	 * @param Context context Context to use for resource localization
	 * @param String dateStr - The db formatted date string, expected to be of the form specified in Utility.DATE_FORMAT
	 * @return a user-friendly representation of the date.
	 */
	public static String getFriendlyDayString(Context context, String dateString) {
		// The day string for forecast uses the following logic:
		// For today: "Today, June 8"
		// For tomorrow: "Tomorrow"
		// For the next 5 days: "Wednesday" (just the day name)
		// For all days after that: "Mon Jun 8"
		Date todayDate = new Date();
		String todayStr = WeatherContract.getDbDateString(todayDate);
		Date inputDate = WeatherContract.getDateFromDb(dateString);
		// If the date we're building the String for is today's date, the format
		// is "Today, June 24"
		if (todayStr.equals(dateString)) {
			String today = context.getString(R.string.today);
			return context.getString(R.string.format_full_friendly_date, today,
					getFormattedMonthDay(context, dateString));
		} else {
			Calendar cal = Calendar.getInstance();
			cal.setTime(todayDate);
			cal.add(Calendar.DATE, 7);
			String weekFutureString = WeatherContract.getDbDateString(cal.getTime());
			if (dateString.compareTo(weekFutureString) < 0) {
				// If the input date is less than a week in the future, just
				// return the day name.
				return getDayName(context, dateString);
			} else {
				// Otherwise, use the form "Mon Jun 3"
				SimpleDateFormat shortenedDateFormat = new SimpleDateFormat(
						"EEE MMM dd", Locale.getDefault());
				return shortenedDateFormat.format(inputDate);
			}
		}
	}
	
	/**
	 * Given a day, returns just the name to use for that day. E.g "today",
	 * "tomorrow", "wednesday".
	 * 
	 * @param Context context - Context to use for resource localization
	 * @param String dateStr - The db formatted date string, expected to be of the form specified in Utility.DATE_FORMAT
	 * @return day name
	 */
	public static String getDayName(Context context, String dateString) {
		SimpleDateFormat dbDateFormat = new SimpleDateFormat(Utility.DATE_FORMAT, Locale.getDefault());
		try {
			Date inputDate = dbDateFormat.parse(dateString);
			Date todayDate = new Date();
			// If the date is today, return the localized version of "Today"
			// instead of the actual
			// day name.
			if (WeatherContract.getDbDateString(todayDate).equals(dateString)) {
				return context.getString(R.string.today);
			} else {
				// If the date is set for tomorrow, the format is "Tomorrow".
				Calendar cal = Calendar.getInstance();
				cal.setTime(todayDate);
				cal.add(Calendar.DATE, 1);
				Date tomorrowDate = cal.getTime();
				if (WeatherContract.getDbDateString(tomorrowDate).equals(dateString)) {
					return context.getString(R.string.tomorrow);
				} else {
					// Otherwise, the format is just the day of the week (e.g
					// "Wednesday".
					SimpleDateFormat dayFormat = new SimpleDateFormat("EEEE", Locale.getDefault());
					return dayFormat.format(inputDate);
				}
			}
		} catch (ParseException e) {
			//e.printStackTrace();
			// It couldn't process the date correctly.
			return "";
		}	
	}

	/**
	 * Converts db date format to the format "Month day", e.g "June 24".
	 * 
	 * @param Context context - Context to use for resource localization
	 * @param String dateStr - The db formatted date string, expected to be of the form
	 *            specified in Utility.DATE_FORMAT
	 * @return The day in the form of a string formatted "December 6"
	 */
	public static String getFormattedMonthDay(Context context, String dateString) {
		SimpleDateFormat dbDateFormat = new SimpleDateFormat(Utility.DATE_FORMAT, Locale.getDefault());
		try {
			Date inputDate = dbDateFormat.parse(dateString);
			SimpleDateFormat monthDayFormat = new SimpleDateFormat("MMMM dd", Locale.getDefault());
			String monthDayString = monthDayFormat.format(inputDate);
			return monthDayString;
		} catch (ParseException e) {
			//e.printStackTrace();
			return null;
		}
	}
	
	public static String getFormattedPressure(Context context, double pressure) {
		return context.getString(R.string.format_pressure, pressure);
	}
	
	public static String getFormattedHumidity(Context context, double humidity) {
		return context.getString(R.string.format_humidity, humidity);
	}
	
	/**
	 * @param Context context
	 * @param float windSpeed
	 * @param float degrees
	 * @return formatted wind speed
	 */
	public static String getFormattedWind(Context context, float windSpeed, float degrees) {
		int windFormat;
		if (Utility.isMetric(context)) {
			windFormat = R.string.format_wind_kmh;
		} else {
			windFormat = R.string.format_wind_mph;
			windSpeed = .621371192237334f * windSpeed;
		}
		// From wind direction in degrees, determine compass direction as a
		// string (e.g NW)
		// You know what's fun, writing really long if/else statements with tons
		// of possible
		// conditions. Seriously, try it!
		String direction = "Unknown";
		if (degrees >= 337.5 || degrees < 22.5) {
			direction = "N";
		} else if (degrees >= 22.5 && degrees < 67.5) {
			direction = "NE";
		} else if (degrees >= 67.5 && degrees < 112.5) {
			direction = "E";
		} else if (degrees >= 112.5 && degrees < 157.5) {
			direction = "SE";
		} else if (degrees >= 157.5 && degrees < 202.5) {
			direction = "S";
		} else if (degrees >= 202.5 && degrees < 247.5) {
			direction = "SW";
		} else if (degrees >= 247.5 && degrees < 292.5) {
			direction = "W";
		} else if (degrees >= 292.5 || degrees < 22.5) {
			direction = "NW";
		}
		return String.format(context.getString(windFormat), windSpeed,
				direction);
	}
	
	/**
	 * @param Context context
	 * @param float windSpeed
	 * @param float degrees
	 * @return formatted wind speed
	 */
	public static String getFormattedWindDirectionOnly(Context context, float windSpeed, float degrees) {
		// From wind direction in degrees, determine compass direction as a
		// string (e.g NW)
		// You know what's fun, writing really long if/else statements with tons
		// of possible
		// conditions. Seriously, try it!
		String direction = UNKNOWN_WIND_DIRECTION;
		if (degrees >= 337.5 || degrees < 22.5) {
			direction = "N";
		} else if (degrees >= 22.5 && degrees < 67.5) {
			direction = "NE";
		} else if (degrees >= 67.5 && degrees < 112.5) {
			direction = "E";
		} else if (degrees >= 112.5 && degrees < 157.5) {
			direction = "SE";
		} else if (degrees >= 157.5 && degrees < 202.5) {
			direction = "S";
		} else if (degrees >= 202.5 && degrees < 247.5) {
			direction = "SW";
		} else if (degrees >= 247.5 && degrees < 292.5) {
			direction = "W";
		} else if (degrees >= 292.5 || degrees < 22.5) {
			direction = "NW";
		}
		return direction;
	}
	
	/**
	 * Helper method to provide the icon resource id according to the weather
	 * condition id returned by the OpenWeatherMap call.
	 * 
	 * @param weatherId from OpenWeatherMap API response
	 * @return resource id for the corresponding icon. -1 if no relation is found.
	 */
	public static int getIconResourceForWeatherCondition(int weatherId) {
		// Based on weather code data found at:
		// http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes
		if (weatherId >= 200 && weatherId <= 232) {
			return R.drawable.ic_storm;
		} else if (weatherId >= 300 && weatherId <= 321) {
			return R.drawable.ic_light_rain;
		} else if (weatherId >= 500 && weatherId <= 504) {
			return R.drawable.ic_rain;
		} else if (weatherId == 511) {
			return R.drawable.ic_snow;
		} else if (weatherId >= 520 && weatherId <= 531) {
			return R.drawable.ic_rain;
		} else if (weatherId >= 600 && weatherId <= 622) {
			return R.drawable.ic_snow;
		} else if (weatherId >= 701 && weatherId <= 761) {
			return R.drawable.ic_fog;
		} else if (weatherId == 761 || weatherId == 781) {
			return R.drawable.ic_storm;
		} else if (weatherId == 800) {
			return R.drawable.ic_clear;
		} else if (weatherId == 801) {
			return R.drawable.ic_light_clouds;
		} else if (weatherId >= 802 && weatherId <= 804) {
			return R.drawable.ic_cloudy;
		}
		return -1;
	}
	 
	/**
	 * Helper method to provide the art resource id according to the weather
	 * condition id returned by the OpenWeatherMap call.
	 * 
	 * @param weatherId from OpenWeatherMap API response
	 * @return resource id for the corresponding image. -1 if no relation is found.
	 */
	public static int getArtResourceForWeatherCondition(int weatherId) {
		// Based on weather code data found at:
		// http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes
		if (weatherId >= 200 && weatherId <= 232) {
			return R.drawable.art_storm;
		} else if (weatherId >= 300 && weatherId <= 321) {
			return R.drawable.art_light_rain;
		} else if (weatherId >= 500 && weatherId <= 504) {
			return R.drawable.art_rain;
		} else if (weatherId == 511) {
			return R.drawable.art_snow;
		} else if (weatherId >= 520 && weatherId <= 531) {
			return R.drawable.art_rain;
		} else if (weatherId >= 600 && weatherId <= 622) {
			return R.drawable.art_rain;
		} else if (weatherId >= 701 && weatherId <= 761) {
			return R.drawable.art_fog;
		} else if (weatherId == 761 || weatherId == 781) {
			return R.drawable.art_storm;
		} else if (weatherId == 800) {
			return R.drawable.art_clear;
		} else if (weatherId == 801) {
			return R.drawable.art_light_clouds;
		} else if (weatherId >= 802 && weatherId <= 804) {
			return R.drawable.art_clouds;
		}
		return -1;
	}
	
}

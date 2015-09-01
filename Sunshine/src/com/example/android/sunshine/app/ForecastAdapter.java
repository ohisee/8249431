/**
 * 
 */
package com.example.android.sunshine.app;

import android.content.Context;
import android.database.Cursor;
import android.support.v4.widget.CursorAdapter;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

/**
 * Represents a custom forecast adapter.
 *
 */
public class ForecastAdapter extends CursorAdapter {
	
	private final int VIEW_TYPE_TODAY = 0;
	private final int VIEW_TYPE_FUTURE_DAY = 1;
	private final int VIEW_TYPE_COUNT = 2;
	
	private boolean mUseTodayLayout = false;

	/**
	 * A custom forecast adapter
	 * @param Context context
	 * @param Cursor cursor
	 * @param int flags
	 */
	public ForecastAdapter(Context context, Cursor cursor, int flags) {
		super(context, cursor, flags);
	}
	
	public void setUserTodayLayout(boolean useTodayLayout) {
		mUseTodayLayout = useTodayLayout;
	}
	
	@Override
	public int getItemViewType(int position) {
		return (position == 0 && mUseTodayLayout) ? VIEW_TYPE_TODAY : VIEW_TYPE_FUTURE_DAY;
	}

	@Override
	public int getViewTypeCount() {
		return VIEW_TYPE_COUNT;
	}

	@Override
	public View newView(Context context, Cursor cursor, ViewGroup rootViewGroup) {
		//return LayoutInflater.from(context).inflate(R.layout.list_item_forecast, rootViewGroup, false);
		// Choose the layout type
		int viewType = getItemViewType(cursor.getPosition());
		
		//Determine layoutId from viewType
		int layoutId = -1;
		if (viewType == VIEW_TYPE_TODAY) {
			layoutId = R.layout.list_item_forecase_today;
		} else if (viewType == VIEW_TYPE_FUTURE_DAY) {
			layoutId = R.layout.list_item_forecast;
		}
		
		View view = LayoutInflater.from(context).inflate(layoutId, rootViewGroup, false);
		ViewHolder viewHolder = new ViewHolder(view);
		view.setTag(viewHolder);
		return view;
	}

	@Override
	public void bindView(View view, Context context, Cursor cursor) {
		
		// Get view from view holder
		ViewHolder viewHolder = (ViewHolder) view.getTag();
		
		// Read weather icon ID from cursor
		int weatherId = cursor.getInt(ForecastFragment.COL_WEATHER_ID);
		
		// Get view type
		int viewType = getItemViewType(cursor.getPosition());
		//Determine layoutId from viewType
		int layoutId = -1;
		if (viewType == VIEW_TYPE_TODAY) {
			layoutId = Utility.getArtResourceForWeatherCondition(weatherId);
		} else if (viewType == VIEW_TYPE_FUTURE_DAY) {
			layoutId = Utility.getIconResourceForWeatherCondition(weatherId);
		}
		
		// Use placeholder image for now
		//ImageView iconView = (ImageView) view.findViewById(R.id.list_item_icon);
		//iconView.setImageResource(R.drawable.ic_launcher);
		//viewHolder.iconView.setImageResource(R.mipmap.ic_launcher);
		
		// User placeholder image
		viewHolder.iconView.setImageResource(layoutId);
		
		// Read date from cursor
		String dateString = cursor.getString(ForecastFragment.COL_WEATHER_DATE);
		
		// Find TextView and set formatted date on it
		//TextView dateView = (TextView) view.findViewById(R.id.list_item_date_textview);
		viewHolder.dateView.setText(Utility.getFriendlyDayString(context, dateString));
		
		// Read weather forecast from cursor
		String description = cursor.getString(ForecastFragment.COL_WEATHER_DESC);
		
		// Find TextView and set weather forecast on it
		//TextView descriptionView = (TextView) view.findViewById(R.id.list_item_forecast_textview);
		viewHolder.descriptionView.setText(description);
		
		// For accessibility, add a content description to the icon field.
		viewHolder.iconView.setContentDescription(description);
		
		// Read user preference for metric or imperial temperature units
		boolean isMetric = Utility.isMetric(context);
		// Read high temperature from cursor
		float high = cursor.getFloat(ForecastFragment.COL_WEATHER_MAX_TEMP);
		// Read low temperature from cursor
		float low = cursor.getFloat(ForecastFragment.COL_WEATHER_MIN_TEMP);
		
		String highTemp = Utility.formatTemperature(context, high, isMetric);
		String lowTemp = Utility.formatTemperature(context, low, isMetric);
		
		//Find TextView and set formatted high temperature on it
		//TextView hiTeView = (TextView) view.findViewById(R.id.list_item_high_textview); 
		//hiTeView.setText(highTemp + "\u00B0");
		viewHolder.highTempView.setText(highTemp);
		
		//Find TextView and set formatted low temperature on it
		//TextView loTeView = (TextView) view.findViewById(R.id.list_item_low_textview);
		//loTeView.setText(lowTemp + "\u00B0");
		viewHolder.lowTempView.setText(lowTemp);
	}
	
	/**
	 * Represents a view holder to avoid unnecessary find by view ID calls. 
	 *
	 */
	public static class ViewHolder {

		public final ImageView iconView;
		public final TextView dateView;
		public final TextView descriptionView;
		public final TextView highTempView;
		public final TextView lowTempView;

		public ViewHolder(View view) {
			iconView = (ImageView) view.findViewById(R.id.list_item_icon);
			dateView = (TextView) view.findViewById(R.id.list_item_date_textview);
			descriptionView = (TextView) view.findViewById(R.id.list_item_forecast_textview);
			highTempView = (TextView) view.findViewById(R.id.list_item_high_textview);
			lowTempView = (TextView) view.findViewById(R.id.list_item_low_textview);
		}
	}

}

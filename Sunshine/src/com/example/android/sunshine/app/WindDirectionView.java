/**
 * 
 */
package com.example.android.sunshine.app;

import java.util.HashMap;
import java.util.Map;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.util.Log;
import android.util.Pair;
import android.view.View;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityManager;

/**
 * Represents a custom view.
 *
 */
public class WindDirectionView extends View {
	
	private static final String LOG_TAG = WindDirectionView.class.getSimpleName();
	
	private float mCx;
	private float mCy;
	private float mOuterRadius, mInnerRadius;
	private Paint mCirclePaint, mLinePaint, mTextPaint;
	private static int VIEW_WIDTH = 120;
	private static int VIEW_HEIGHT = 120;
	private static int MAX_WIDTH = VIEW_WIDTH - 20;
	private static int MAX_HEIGHT = VIEW_HEIGHT - 20;
	private String mDirection;
	private Map<String, Pair<Float, Float>> directions = new HashMap<String, Pair<Float, Float>>();
	private Map<String, Integer> angles = new HashMap<String, Integer>();
	private AccessibilityManager mAccessibilityManager;
	
	public WindDirectionView(Context context) {
		super(context);
		init(context);
	}

	public WindDirectionView(Context context, AttributeSet attrs, int defStyleAttr) {
		super(context, attrs, defStyleAttr);
		init(context);
	}

	public WindDirectionView(Context context, AttributeSet attrs) {
		super(context, attrs);
		init(context);
	}

	/**
	 * Trying to initialize this view
	 * @param Context context
	 */
	private void init (Context context) {
		mCirclePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
		mCirclePaint.setColor(Color.BLUE);
		mCirclePaint.setStyle(Paint.Style.STROKE);
		mCirclePaint.setStrokeWidth(2.0f);
		mTextPaint = new Paint(Paint.LINEAR_TEXT_FLAG);
		mTextPaint.setColor(Color.BLACK);
		mTextPaint.setStyle(Paint.Style.STROKE);
		mTextPaint.setStrokeWidth(1.0f);
		mLinePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
		mLinePaint.setColor(Color.RED);
		mLinePaint.setStyle(Paint.Style.STROKE);
		mLinePaint.setStrokeWidth(3.0f);
		mCx = VIEW_WIDTH / 2; // Center of VIEW
		mCy = VIEW_HEIGHT / 2; // Center of VIEW
		mOuterRadius = MAX_HEIGHT / 2;
		mInnerRadius = mOuterRadius - 10;
		
		buildDirections();
		buildEvent(context);
	}

	@Override
	protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
		// TODO Auto-generated method stub
		super.onMeasure(widthMeasureSpec, heightMeasureSpec);
		
		int hSpecMode = MeasureSpec.getMode(heightMeasureSpec);
		int hSpecSize = MeasureSpec.getSize(heightMeasureSpec);
		int myHeight = hSpecSize;
		
		int wSpecMode = MeasureSpec.getMode(widthMeasureSpec);
		int wSpecSize = MeasureSpec.getSize(widthMeasureSpec);
		int myWidth = wSpecSize;		
		
		if (hSpecMode == MeasureSpec.EXACTLY) {
			myHeight = hSpecSize;
		} else if (hSpecMode == MeasureSpec.AT_MOST) {
			myHeight = Math.min(VIEW_WIDTH, hSpecSize);
		} else {
			myHeight = VIEW_WIDTH;
		}
		
		if (wSpecMode == MeasureSpec.EXACTLY) {
			myWidth = wSpecSize;
		} else if (wSpecMode == MeasureSpec.AT_MOST) {
			myWidth = Math.min(VIEW_HEIGHT, wSpecSize);
		} else {
			myWidth = VIEW_HEIGHT;
		}
		
		setMeasuredDimension(myWidth, myHeight);
	}

	@Override
	protected void onDraw(Canvas canvas) {
		// TODO Auto-generated method stub
		super.onDraw(canvas);
		
		//canvas.drawCircle(mCx, mCy, mOuterRadius, mCirclePaint);
		canvas.drawCircle(mCx, mCy, mInnerRadius, mCirclePaint);
		
		Pair<Float, Float> pair = directions.get("E");
		canvas.drawText("E", pair.first, pair.second, mTextPaint);

		pair = directions.get("SE");
		canvas.drawText("SE", pair.first, pair.second, mTextPaint);
		
		pair = directions.get("S");
		canvas.drawText("S", pair.first, pair.second, mTextPaint);
		
		pair = directions.get("SW");
		canvas.drawText("SW", pair.first, pair.second, mTextPaint);
		
		pair = directions.get("W");
		canvas.drawText("W", pair.first, pair.second, mTextPaint);
		
		pair = directions.get("NW");
		canvas.drawText("NW", pair.first, pair.second, mTextPaint);
		
		pair = directions.get("N");
		canvas.drawText("N", pair.first, pair.second, mTextPaint);
		
		pair = directions.get("NE");
		canvas.drawText("NE", pair.first, pair.second, mTextPaint);
		
		if (null != mDirection) {
			Integer angle = angles.get(mDirection);
			if (null != angle) {
				float x = (mCx) + (mInnerRadius) * (float) Math.cos(angle * Math.PI / 180);
				float y = (mCy) + (mInnerRadius) * (float) Math.sin(angle * Math.PI / 180);
				canvas.drawLine(mCx, mCy, x, y, mLinePaint);
			}
		}
	}
	
	/**
	 * Trying to build the wind direction
	 */
	private void buildDirections() {
		int angleStart = 45;
		int angle = 0;
		int offsetY = 7;
		int offsetX = 7;
		
		float x = (mCx) + (mOuterRadius) * (float) Math.cos(angle * Math.PI / 180);
		float y = (mCy) + (mOuterRadius) * (float) Math.sin(angle * Math.PI / 180);
		if (!directions.containsKey("E")) {
			directions.put("E", new Pair<Float, Float>(x, y));
			angles.put("E", angle);
		}
		
		angle = angle + angleStart;
		x = (mCx) + (mOuterRadius) * (float) Math.cos(angle * Math.PI / 180);
		y = (mCy) + (mOuterRadius) * (float) Math.sin(angle * Math.PI / 180);
		if (!directions.containsKey("SE")) {
			directions.put("SE", new Pair<Float, Float>(x - offsetX, y));
			angles.put("SE", angle);
		}
		
		angle = angle + angleStart;
		x = (mCx) + (mOuterRadius) * (float) Math.cos(angle * Math.PI / 180);
		y = (mCy) + (mOuterRadius) * (float) Math.sin(angle * Math.PI / 180);
		if (!directions.containsKey("S")) {
			directions.put("S", new Pair<Float, Float>(x - 3, y + offsetY));
			angles.put("S", angle);
		}
		
		angle = angle + angleStart;
		x = (mCx) + (mOuterRadius) * (float) Math.cos(angle * Math.PI / 180);
		y = (mCy) + (mOuterRadius) * (float) Math.sin(angle * Math.PI / 180);
		if (!directions.containsKey("SW")) {
			directions.put("SW", new Pair<Float, Float>(x - offsetX * 2, y));
			angles.put("SW", angle);
		}
		
		angle = angle + angleStart;
		x = (mCx) + (mOuterRadius) * (float) Math.cos(angle * Math.PI / 180);
		y = (mCy) + (mOuterRadius) * (float) Math.sin(angle * Math.PI / 180);
		if (!directions.containsKey("W")) {
			directions.put("W", new Pair<Float, Float>(x - offsetX, y));
			angles.put("W", angle);
		}
		
		angle = angle + angleStart;
		x = (mCx) + (mOuterRadius) * (float) Math.cos(angle * Math.PI / 180);
		y = (mCy) + (mOuterRadius) * (float) Math.sin(angle * Math.PI / 180);
		if (!directions.containsKey("NW")) {
			directions.put("NW", new Pair<Float, Float>(x - offsetX, y + 2));
			angles.put("NW", angle);
		}
		
		angle = angle + angleStart;
		x = (mCx) + (mOuterRadius) * (float) Math.cos(angle * Math.PI / 180);
		y = (mCy) + (mOuterRadius) * (float) Math.sin(angle * Math.PI / 180);
		if (!directions.containsKey("N")) {
			directions.put("N", new Pair<Float, Float>(x - 3, y));
			angles.put("N", angle);
		}
		
		angle = angle + angleStart;
		x = (mCx) + (mOuterRadius) * (float) Math.cos(angle * Math.PI / 180);
		y = (mCy) + (mOuterRadius) * (float) Math.sin(angle * Math.PI / 180);
		if (!directions.containsKey("NE")) {
			directions.put("NE", new Pair<Float, Float>(x - offsetX - 2, y + 2));
			angles.put("NE", angle);
		}
	}
	
	/**
	 * Trying to set the wind direction
	 * @param String direction
	 */
	public void setDirection(String direction) {
		mDirection = direction;
		setContentDescription(mDirection);
		sendEvent();
	}
	
	/**
	 * Trying to build accessibility manager
	 * @param Context context
	 */
	private void buildEvent(Context context) {
		if (null != context) {
			mAccessibilityManager = (AccessibilityManager) context.getSystemService(Context.ACCESSIBILITY_SERVICE);
		} else {
			Log.i(LOG_TAG, "Context is not available");
		}
	}
	
	/**
	 * Trying to send an event
	 */
	private void sendEvent() {
		if (null != mAccessibilityManager) {
			if (mAccessibilityManager.isEnabled()) {
				sendAccessibilityEvent(AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED);
			} else {
				Log.i(LOG_TAG, "Accessibility Manager is not enabled");
			}
		} else {
			Log.i(LOG_TAG, "Accessibility Manager is not available");
		}		
	}

	@Override
	public boolean dispatchPopulateAccessibilityEvent(AccessibilityEvent event) {
		super.dispatchPopulateAccessibilityEvent(event);
		if (null != mDirection) {
			event.getText().add(mDirection);
			Log.i(LOG_TAG, "Wind Direction");
		}
		return true;
	}

}

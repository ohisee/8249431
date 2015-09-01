/**
 * 
 */
package com.example.android.sunshine.app;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.MeasureSpec;

/**
 * Pie View
 *
 */
public class PieView extends View {
	
	private int VIEW_WIDTH = 120;
	private int VIEW_HEIGHT = 120;
	private Paint mCirclePaint, mLinePaint;
	private float centerX, centerY, circleRadius;

	public PieView(Context context) {
		super(context);
		initializePaint();
	}

	public PieView(Context context, AttributeSet attrs, int defStyleAttr) {
		super(context, attrs, defStyleAttr);
		initializePaint();
	}

	public PieView(Context context, AttributeSet attrs) {
		super(context, attrs);
		initializePaint();
	}
	
	/**
	 * 
	 */
	private void initializePaint() {
		mCirclePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
		mCirclePaint.setColor(Color.GREEN);
		mCirclePaint.setStyle(Paint.Style.STROKE);
		mCirclePaint.setStrokeWidth(2.0f);
		mLinePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
		mLinePaint.setColor(Color.RED);
		mLinePaint.setStyle(Paint.Style.STROKE);
		mLinePaint.setStrokeWidth(3.0f);
		centerX = getWidth();
		centerY = getHeight();
		circleRadius = 30;
	}
	
	/**
	 * Override onMeasure
	 */
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

	/**
	 * Override onDraw
	 */
	@Override
	protected void onDraw(Canvas canvas) {
		// TODO Auto-generated method stub
		super.onDraw(canvas);
		canvas.drawCircle(centerX, centerY, circleRadius, mCirclePaint);
	}

}

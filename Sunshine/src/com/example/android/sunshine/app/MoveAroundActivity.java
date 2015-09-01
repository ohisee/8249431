/**
 * 
 */
package com.example.android.sunshine.app;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.os.Bundle;
import android.support.v4.view.GestureDetectorCompat;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.view.animation.Interpolator;
import android.view.animation.OvershootInterpolator;
import android.widget.FrameLayout;

/**
 * Move Around Activity 
 *
 */
public class MoveAroundActivity extends ActionBarActivity {
	
	private static final String LOG_TAG = MoveAroundActivity.class.getSimpleName();
	
	//private ImageView iconView;
	//private int mActivePointerId = -1;
	//private float mLastTouchX = 0, mLastTouchY = 0;
	
	/**
	 * 
	 */
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.move_around_main);
		FrameLayout frameLayout = (FrameLayout) findViewById(R.id.imageMovableHolder);
		MovableView view = new MovableView(this);
		frameLayout.addView(view);
	}
	
	/**
	 * 
	 */
	@Override
	protected void onStop() {
		// TODO Auto-generated method stub
		super.onStop();
	}
	
	/**
	 * Movable View
	 */
	private class MovableView extends View {
		
		private GestureDetectorCompat mGestureDetector;
		private Matrix translate;
		private Bitmap iView;
		
		private Matrix animateStart;
		private Interpolator animateInterpolator;
		private long startTime;
		private long endTime;
		private float totalAnimateDx;
		private float totalAnimateDy;
		
		/**
		 * View constructor
		 * @param Context context
		 */
		public MovableView(Context context) {
			super(context);
			translate = new Matrix();
			mGestureDetector = new GestureDetectorCompat(context,
					new MyGestureListener(this));
			iView = BitmapFactory.decodeResource(getResources(),
					R.drawable.play);
			// To call this view's onDraw
			setWillNotDraw(false);
		}
		
		@Override
		protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
			int parentWidth = MeasureSpec.getSize(widthMeasureSpec);
			int parentHeight = MeasureSpec.getSize(heightMeasureSpec);
			this.setMeasuredDimension(parentWidth, parentHeight);
			super.onMeasure(widthMeasureSpec, heightMeasureSpec);
		}

		/**
		 * @param float dx
		 * @param float dy
		 * @param long duration
		 */
		public void onAnimateMove(float dx, float dy, long duration) {
			animateStart = new Matrix(translate);
			animateInterpolator = new OvershootInterpolator();
			startTime = System.currentTimeMillis();
			endTime = startTime + duration;
			totalAnimateDx = dx;
			totalAnimateDy = dy;
			
			post(new Runnable() {
				@Override
				public void run() {
					onAnimateStep();
				}
			});
		}
		
		/**
		 * 
		 */
        private void onAnimateStep() {
            long curTime = System.currentTimeMillis();
            float percentTime = (float) (curTime - startTime) / (float) (endTime - startTime);
            float percentDistance = animateInterpolator.getInterpolation(percentTime);
            float curDx = percentDistance * totalAnimateDx;
            float curDy = percentDistance * totalAnimateDy;
            translate.set(animateStart);
            onMove(curDx, curDy);
            
//            if (percentTime < 1.0f) {
//                post(new Runnable() {
//                    @Override
//                    public void run() {
//                        onAnimateStep();
//                    }
//                });
//            }
        }
        
//        @TargetApi(Build.VERSION_CODES.HONEYCOMB) 
        public void onMove(float dx, float dy) {
        	Log.d(LOG_TAG, "View On Move");
        	translate.postTranslate(dx, dy);
//        	if (Build.VERSION.SDK_INT >= 11) {
//        		if (isDirty()) {
//        			Log.d(LOG_TAG, "View On Move changed");
//        		}
//        	}
        	invalidate();
        }
        
        public void onResetLocation() {
        	Log.d(LOG_TAG, "View On Reset Location");
        	translate.reset();
        	invalidate();
        }
        
//        public void onSetLocation(float dx, float dy) {
//        	translate.postTranslate(dx, dy);
//        }

		@Override
		protected void onDraw(Canvas canvas) {
			super.onDraw(canvas);
			Log.d(LOG_TAG, "View On Draw");
			canvas.drawBitmap(iView, translate, null);
		}

		@Override
		public boolean onTouchEvent(MotionEvent event) {
			performClick();
			return mGestureDetector.onTouchEvent(event);
		}

		@Override
		public boolean performClick() {
			return super.performClick();
		}
		
	}
	
	/**
	 * Gesture Listener
	 */
	private class MyGestureListener extends GestureDetector.SimpleOnGestureListener {
		
		private final String LOG_GS_TAG = MyGestureListener.class.getSimpleName();
		
		MovableView view;
		
		public MyGestureListener(MovableView view) {
			this.view = view;
		}

		@Override
		public boolean onDoubleTap(MotionEvent e) {
			Log.d(LOG_GS_TAG, "onDoubleTap");
			view.onResetLocation();
			return true;
		}

		@Override
		public boolean onDoubleTapEvent(MotionEvent e) {
			Log.d(LOG_GS_TAG, "onDoubleTapEvent");
			return super.onDoubleTapEvent(e);
		}

		@Override
		public boolean onDown(MotionEvent e) {
			Log.d(LOG_GS_TAG, "onDown return true");
			return true;
		}

		@Override
		public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX,
				float velocityY) {
			Log.d(LOG_GS_TAG, "onFling");
			final float distanceTimeFactor = 0.4f;
			final float totalDx = (distanceTimeFactor * velocityX / 2);
			final float totalDy = (distanceTimeFactor * velocityY / 2);
			view.onAnimateMove(totalDx, totalDy, (long) (1000 * distanceTimeFactor));
			return true;
		}

		@Override
		public void onLongPress(MotionEvent e) {
			Log.d(LOG_GS_TAG, "onLongPress");
			super.onLongPress(e);
		}

		@Override
		public boolean onScroll(MotionEvent e1, MotionEvent e2,
				float distanceX, float distanceY) {
			Log.d(LOG_GS_TAG, "onScroll " + distanceX + " " + distanceY);
			view.onMove(-distanceX, -distanceY);
			return true;
		}

		@Override
		public void onShowPress(MotionEvent e) {
			Log.d(LOG_GS_TAG, "onShowPress");
			super.onShowPress(e);
		}

		@Override
		public boolean onSingleTapConfirmed(MotionEvent e) {
			Log.d(LOG_GS_TAG, "onSingleTapConfirmed");
			return super.onSingleTapConfirmed(e);
		}

		@Override
		public boolean onSingleTapUp(MotionEvent e) {
			Log.d(LOG_GS_TAG, "onSingleTapUp");
			return super.onSingleTapUp(e);
		}
	}
	
}


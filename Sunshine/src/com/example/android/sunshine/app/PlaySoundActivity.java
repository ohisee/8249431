/**
 * 
 */
package com.example.android.sunshine.app;

import android.content.res.AssetFileDescriptor;
import android.media.AudioManager;
import android.media.SoundPool;
import android.media.SoundPool.OnLoadCompleteListener;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageView;

/**
 * This is an activity.
 *
 */
public class PlaySoundActivity extends ActionBarActivity {
	
	private final String LOG_TAG = PlaySoundActivity.class.getSimpleName();
	
	private ImageView iconView;
	private SoundPool soundPool;
	private int soundId;
	private boolean loaded = false;

	/**
	 * @param Bundle savedInstanceState
	 */
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.play_sound_main);
		iconView = (ImageView) findViewById(R.id.imageViewPlay);
		if (null != iconView) {
			prepareSound();
			iconView.setOnClickListener(new OnClickListener() {
				@Override
				public void onClick(View v) {
					playSound();
				}
			});
		}
	}

	/**
	 * Release the sound pool on stop.
	 */
	@Override
	protected void onStop() {
		super.onStop();
		if (null != soundPool) {
			soundPool.release();
			soundPool = null;
		}
	}
	
	/**
	 * 
	 */
	private void prepareSound() {
		try {
			AssetFileDescriptor afd = getAssets().openFd("movie_quote.mp3");
			//AudioManager audioManager = (AudioManager) getSystemService(AUDIO_SERVICE);
			setVolumeControlStream(AudioManager.STREAM_MUSIC);
			soundPool = new SoundPool(1, AudioManager.STREAM_MUSIC, 0);
			soundPool.setOnLoadCompleteListener(new OnLoadCompleteListener() {
				@Override
				public void onLoadComplete(SoundPool soundPool, int sampleId, int status) {
					loaded = true;
				}
			});
			soundId = soundPool.load(afd, 1);
		} catch (Exception e) {
			Log.e(LOG_TAG, e.getMessage());
		}
	}
	
	/**
	 * 
	 */
	private void playSound() {
		if (loaded) {
			soundPool.stop(soundId);
			soundPool.play(soundId, 1.0f, 1.0f, 0, 0, 1.0f);
		}
	}
	
}

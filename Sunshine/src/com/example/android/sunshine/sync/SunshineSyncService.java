/**
 * 
 */
package com.example.android.sunshine.sync;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

/**
 * Represents sunshine sync service.
 *
 */
public class SunshineSyncService extends Service {
	
	private static final Object sSyncAdaterLock = new Object();
	private static SunshineSyncAdapter sSunshineSyncAdapter = null;

	@Override
	public void onCreate() {
		Log.d("SunshineSyncService", "onCreate - SunshineSyncService");
		synchronized (sSyncAdaterLock) {
			if (null == sSunshineSyncAdapter) {
				sSunshineSyncAdapter = new SunshineSyncAdapter(getApplicationContext(), true);
			}
		}
	}

	@Override
	public IBinder onBind(Intent intent) {
		return sSunshineSyncAdapter.getSyncAdapterBinder();
	}

}

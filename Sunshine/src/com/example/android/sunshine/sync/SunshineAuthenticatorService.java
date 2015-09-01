/**
 * 
 */
package com.example.android.sunshine.sync;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

/**
 * Represents sunshine authenticator service.
 *
 */
public class SunshineAuthenticatorService extends Service {
	
	private SunshineAuthenticator mAuthenticator;

	@Override
	public void onCreate() {
		mAuthenticator = new SunshineAuthenticator(this);
	}

	@Override
	public IBinder onBind(Intent intent) {
		return mAuthenticator.getIBinder();
	}

}

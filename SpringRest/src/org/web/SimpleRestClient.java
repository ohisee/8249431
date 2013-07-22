/**
 * 
 */
package org.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.items.RootAddress;


/**
 * 
 *
 */
@Component("simpleRestClient")
public class SimpleRestClient {
	
	private static Log logger = LogFactory.getLog(SimpleRestClient.class);
	
	public RootAddress invokeRestUrl(String url) {
		if (logger.isDebugEnabled()) {
			logger.debug("Ready to call URL");
		}
		RootAddress result = restTemplate.getForObject(url, RootAddress.class);
		return result;
	}
	
	@Autowired
	private RestTemplate restTemplate;
}

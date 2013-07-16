/**
 * 
 */
package org.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;


/**
 * 
 *
 */

@Component("simpleRestClient")
public class SimpleRestClient {
	
	private static Log logger = LogFactory.getLog(SimpleRestClient.class);
	
	public String invokeRestUrl(String url) {
		if (logger.isDebugEnabled()) {
			logger.debug("Ready to call URL");
		}
		String result = restTemplate.getForObject(url, String.class);
		return result;
	}
	
	@Autowired
	private RestTemplate restTemplate;
}

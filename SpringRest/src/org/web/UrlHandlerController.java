/**
 * 
 */
package org.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.items.RootAddress;


/**
 * 
 *
 */
@Controller
public class UrlHandlerController {

	private static Log logger = LogFactory.getLog(UrlHandlerController.class);
	
	@RequestMapping(value = "/callrest", method = RequestMethod.GET)
	@ResponseBody
	public RootAddress getUrlFromUI(@RequestParam("resturl") String url ) {
		
		logger.info("METHOD GET - getUrlFromUI -");
		logger.info("URL is " + url);
		
		RootAddress s = simpleRestClient.invokeRestUrl(url);
		
		return s;
	}

	
	@Autowired
	private SimpleRestClient simpleRestClient;
}

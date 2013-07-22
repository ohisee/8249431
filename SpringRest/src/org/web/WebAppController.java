/**
 * 
 */
package org.web;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;

import org.springframework.stereotype.Controller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import org.services.ItemService;
import org.items.Item;
import org.items.RootAddress;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;


/**
 * 
 *
 */
@Controller
@RequestMapping (value = WebAppUrls.ROOT_URL)
public class WebAppController {
	
	private static Log logger = LogFactory.getLog(WebAppController.class);
	
	@RequestMapping (value = WebAppUrls.URL_ITEM, method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
	@ResponseBody
	public Item getItem(@PathVariable String identifier) {
		if (logger.isDebugEnabled()) {
			logger.debug("Method GET - getItem");
		}
		return itemService.getItem(identifier);
	}
	
	@RequestMapping (value = WebAppUrls.URL_GET_ITEM, method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
	@ResponseBody
	public RootAddress getAddressItem(@RequestParam String resturl) {
		
		logger.info("Method GET - getAddressItem");
		logger.info(resturl);
		try {
			resturl = URLDecoder.decode(resturl, "UTF-8");
		} catch (UnsupportedEncodingException e) {
		}
		logger.info(resturl);
		RootAddress adr = simpleRestClient.invokeRestUrl(resturl);
		return adr;
	}
	
	@RequestMapping (value = WebAppUrls.URL_ADD_ITEM, method = RequestMethod.POST, consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
	@ResponseBody
	public String newAddressItem(@RequestBody RootAddress adr) {
		
		logger.info("Method POST - newAddressItem");
		String ad = null;
		try {
			ad = objectMapper.writer().withDefaultPrettyPrinter().writeValueAsString(adr);
			logger.info(ad);
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		}
		return ad;
	}
	
	@RequestMapping (value = WebAppUrls.URL_UPDATE_ITEM, method = RequestMethod.PUT, produces = MediaType.APPLICATION_JSON_VALUE)
	@ResponseBody
	public String updateAddressItem(@RequestBody String adr) {
		
		logger.info("Method PUT - newAddressItem");
		logger.info("Method PUT - newAddressItem"  + adr);
		
		return adr;
	}
	
	@Autowired
	private ItemService itemService;
	
	@Autowired
	private SimpleRestClient simpleRestClient;
	
	@Autowired
	private ObjectMapper objectMapper;
}

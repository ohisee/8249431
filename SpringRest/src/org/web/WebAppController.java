/**
 * 
 */
package org.web;

import org.springframework.stereotype.Controller;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import org.services.ItemService;
import org.items.Item;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;


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
	
	
	private ItemService itemService;
	
	@Autowired
	public void setItemService(ItemService itemService) {
		this.itemService = itemService;
	}
}

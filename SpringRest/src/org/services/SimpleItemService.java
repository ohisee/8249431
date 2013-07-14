/**
 * 
 */
package org.services;


import org.springframework.stereotype.Service;
import org.items.Item;

/**
 * 
 *
 */
@Service
public class SimpleItemService implements ItemService {

	@Override
	public Item getItem(String identifier) {
		return new Item(identifier);
	}

}

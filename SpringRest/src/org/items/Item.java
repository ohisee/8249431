/**
 * 
 */
package org.items;

/**
 * 
 *
 */
public class Item {
	
	private String identifer;
	private String[] details;
	
	public Item() {}

	public Item(String identifer) {
		super();
		this.identifer = identifer;
		if (null != identifer && !identifer.isEmpty()) {
			//(?!X) X, via zero-width negative lookahead
			details = identifer.split("(?!^)");
		}
	}

	public String getIdentifer() {
		return identifer;
	}

	public void setIdentifer(String identifer) {
		this.identifer = identifer;
	}

	public String[] getDetails() {
		return details;
	}

	public void setDetails(String[] details) {
		this.details = details;
	}
}

/**
 * 
 */
package org.items;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonAutoDetect.Visibility;

/**
 * 
 *
 */
@JsonAutoDetect(fieldVisibility = Visibility.ANY)
@JsonIgnoreProperties(ignoreUnknown = true)
public class RootAddress {
	
	private List<AddressComponents> results;
	private String status;
	
	public RootAddress () {
	}
	
	public List<AddressComponents> getResults() {
		return results;
	}
	public void setResults(List<AddressComponents> results) {
		this.results = results;
	}
	public String getStatus() {
		return status;
	}
	public void setStatus(String status) {
		this.status = status;
	}
}

class AddressComponents {
	
	private AddressComponent[] address_components;
	private String formatted_address;
	private Geometry geometry;
	private String[] types;
	
	public AddressComponents () {
	}
	
	public AddressComponent[] getAddress_components() {
		return address_components;
	}
	public void setAddress_components(AddressComponent[] address_components) {
		this.address_components = address_components;
	}
	public String getFormatted_address() {
		return formatted_address;
	}
	public void setFormatted_address(String formatted_address) {
		this.formatted_address = formatted_address;
	}
	public Geometry getGeometry() {
		return geometry;
	}
	public void setGeometry(Geometry geometry) {
		this.geometry = geometry;
	}
	public String[] getTypes() {
		return types;
	}
	public void setTypes(String[] types) {
		this.types = types;
	}
}

class AddressComponent {
	
	private String long_name;
	private String short_name;
	private String[] types;
	
	public AddressComponent() {
	}
	
	public String getLong_name() {
		return long_name;
	}
	public void setLong_name(String long_name) {
		this.long_name = long_name;
	}
	public String getShort_name() {
		return short_name;
	}
	public void setShort_name(String short_name) {
		this.short_name = short_name;
	}
	public String[] getTypes() {
		return types;
	}
	public void setTypes(String[] types) {
		this.types = types;
	}
}

class Location {
	
	protected double lat;
	protected double lng;
	
	public Location() {
	}
	
	public double getLat() {
		return lat;
	}
	public void setLat(double lat) {
		this.lat = lat;
	}
	public double getLng() {
		return lng;
	}
	public void setLng(double lng) {
		this.lng = lng;
	}
	
	public String toString() {
		return String.format("\"lat\" : %1$.14f, \"lng\" : %2$.14f", lat, lng);
	}
}

class Northeast extends Location {
	public Northeast() {
		super();
	}
}

class Southwest  extends Location {
	public Southwest() {
		super();
	}
}


class Viewport {
	
	private Northeast northeast;
	private Southwest southwest;
	
	public Viewport () {
	}
	
	public Northeast getNortheast() {
		return northeast;
	}
	public void setNortheast(Northeast northeast) {
		this.northeast = northeast;
	}
	public Southwest getSouthwest() {
		return southwest;
	}
	public void setSouthwest(Southwest southwest) {
		this.southwest = southwest;
	}
}

class Geometry {
	
	private Location location;
	private String location_type;
	private Viewport viewport;
	
	public Geometry () {
	}
	
	public Location getLocation() {
		return location;
	}
	public void setLocation(Location location) {
		this.location = location;
	}
	public String getLocation_type() {
		return location_type;
	}
	public void setLocation_type(String location_type) {
		this.location_type = location_type;
	}
	public Viewport getViewport() {
		return viewport;
	}
	public void setViewport(Viewport viewport) {
		this.viewport = viewport;
	}
	
}


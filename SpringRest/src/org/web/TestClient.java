package org.web;

import java.util.List;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonAutoDetect.Visibility;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.core.util.DefaultPrettyPrinter;


@JsonAutoDetect(fieldVisibility = Visibility.ANY)
@JsonIgnoreProperties(ignoreUnknown = true)
class TempJsonObject {
	
	private List<Object> results;
	private String status;
	
	public TempJsonObject () {
	}
	
	public List<Object> getResults() {
		return results;
	}
	public void setResults(List<Object> results) {
		this.results = results;
	}
	public String getStatus() {
		return status;
	}
	public void setStatus(String status) {
		this.status = status;
	}
}

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:applicationContext.xml", "classpath:rest-servlet.xml"})
public class TestClient {
	
	@Autowired
	private RestTemplate restTemplate;
	
	@Test
	public void test() {
		TempJsonObject c = restTemplate.getForObject(
				"http://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false",
				TempJsonObject.class);
		
		DefaultPrettyPrinter dp = new DefaultPrettyPrinter();
	}
}

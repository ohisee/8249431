package org.web;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpEntity;
import org.springframework.http.MediaType;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.items.RootAddress;


@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:test-rest-ws.xml"})
public class TestClient {
	
	@Autowired
	private RestTemplate restTemplate;
	
	@Autowired
	private ObjectMapper objectMapper;
	
	@Autowired
	private RestTemplate restTemplateString;
	
	private static String gmapURL = "http://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false";
	private static String gmapNURL = "http://maps.googleapis.com/maps/api/geocode/json?address=3975+Freedom+Circle,+Santa+Clara,+CA&sensor=false";
	private static String restGetURL = "http://localhost:8080/SpringRest/services/item/addr?resturl=";
	private static String restPostURL = "http://localhost:8080/SpringRest/services/item/newaddr";
	private static String restPutURL = "http://localhost:8080/SpringRest/services/item/updateaddr";
	
	@Test
	public void test() {
		try {
			RootAddress c = restTemplate.getForObject(gmapURL, RootAddress.class);
			System.out.println(objectMapper.writer().withDefaultPrettyPrinter().writeValueAsString(c));
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		}
	}
	
	@Test
	public void testGET() {
		try {
			RootAddress c = restTemplate.getForObject(restGetURL + URLEncoder.encode(gmapURL, "UTF-8"), RootAddress.class);
			System.out.println(objectMapper.writer().withDefaultPrettyPrinter().writeValueAsString(c));
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		} catch (RestClientException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
	}
	
	
	@Test
	public void testPOST() {
		try {
			RootAddress c = restTemplate.getForObject(gmapNURL, RootAddress.class);
			restTemplate.postForObject(restPostURL, c, RootAddress.class);
			System.out.println(objectMapper.writer().withDefaultPrettyPrinter().writeValueAsString(c));
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		} catch (RestClientException e) {
			e.printStackTrace();
		}
	}
	
	@Test
	public void testPUT () {
		try {
			HttpHeaders httpHeaders = new HttpHeaders();
			httpHeaders.setContentType(MediaType.APPLICATION_JSON);
			String jstr = restTemplateString.getForObject(gmapNURL, String.class);
			HttpEntity<String> httpEntity = new HttpEntity<String>(jstr, httpHeaders);
			
			
			restTemplate.put(restPutURL, httpEntity);	
		} catch (RestClientException e) {
			e.printStackTrace();
		}
	}
}

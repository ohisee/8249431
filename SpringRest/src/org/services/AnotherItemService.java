/**
 * 
 */
package org.services;


import org.springframework.stereotype.Service;
import org.items.Item;

/**
Jul 15, 2013 11:35:23 AM org.apache.catalina.core.ApplicationContext log
SEVERE: StandardWrapper.Throwable
org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'webAppController': Injection of autowired dependencies failed; nested exception is org.springframework.beans.factory.BeanCreationException: Could not autowire method: public void org.web.WebAppController.setItemService(org.services.ItemService); nested exception is org.springframework.beans.factory.NoUniqueBeanDefinitionException: No qualifying bean of type [org.services.ItemService] is defined: expected single matching bean but found 2: anotherItemService,simpleItemService
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessPropertyValues(AutowiredAnnotationBeanPostProcessor.java:288)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1122)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:522)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:461)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:295)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:223)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:292)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:194)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:626)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:932)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:479)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:651)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:599)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:665)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:518)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:459)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:136)
	at javax.servlet.GenericServlet.init(GenericServlet.java:160)
	at org.apache.catalina.core.StandardWrapper.initServlet(StandardWrapper.java:1280)
	at org.apache.catalina.core.StandardWrapper.loadServlet(StandardWrapper.java:1193)
	at org.apache.catalina.core.StandardWrapper.load(StandardWrapper.java:1088)
	at org.apache.catalina.core.StandardContext.loadOnStartup(StandardContext.java:5176)
	at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5460)
	at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:150)
	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1559)
	at org.apache.catalina.core.ContainerBase$StartChild.call(ContainerBase.java:1549)
	at java.util.concurrent.FutureTask$Sync.innerRun(FutureTask.java:303)
	at java.util.concurrent.FutureTask.run(FutureTask.java:138)
	at java.util.concurrent.ThreadPoolExecutor$Worker.runTask(ThreadPoolExecutor.java:895)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:918)
	at java.lang.Thread.run(Thread.java:662)
Caused by: org.springframework.beans.factory.BeanCreationException: Could not autowire method: public void org.web.WebAppController.setItemService(org.services.ItemService); nested exception is org.springframework.beans.factory.NoUniqueBeanDefinitionException: No qualifying bean of type [org.services.ItemService] is defined: expected single matching bean but found 2: anotherItemService,simpleItemService
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredMethodElement.inject(AutowiredAnnotationBeanPostProcessor.java:601)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:87)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessPropertyValues(AutowiredAnnotationBeanPostProcessor.java:285)
	... 30 more
 */
@Service
public class AnotherItemService { 
//	implements ItemService {
//
//	@Override
//	public Item getItem(String identifier) {
//		return new Item("New " + identifier);
//	}
}

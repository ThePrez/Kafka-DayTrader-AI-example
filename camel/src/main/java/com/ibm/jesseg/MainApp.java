package com.ibm.jesseg;

import java.util.concurrent.atomic.AtomicInteger;

import org.apache.camel.CamelContext;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.impl.DefaultCamelContext;
import org.apache.camel.component.jt400.Jt400Component;


/**
 * A Camel Application that routes messages from an IBM i data queue to a Kafka server.
 */
public class MainApp { 
    public static void main(final String... args) throws Exception {

        // This class simply reads values and creates URIs from the config.properties file.
        // This is not a standard Camel class, but is part of this example. You can feel free
        // to just write the URIs instead of using this class.
        DtaQToKafkaConfig conf = new DtaQToKafkaConfig();

        // Standard for a Camel deployment. Start by getting a CamelContext object.
        CamelContext context = new DefaultCamelContext();
        System.out.println("Apache Camel version "+context.getVersion());

        // Now, it's pretty simple to define a Camel route!!
        // All the real work is done here. See the README.md for more information.
        final String dtaqUri = conf.getDtaQUri(); //something like -> jt400://username:password@localhost/qsys.lib/mylib.lib/myq.DTAQ?keyed=false&format=binary&guiAvailable=false
        final String kafkaUri = conf.getKafkaUri(); //something like -> kafka:mytopic?brokers=mybroker:9092
        final AtomicInteger ctr = new AtomicInteger(0);
        context.addRoutes(new RouteBuilder() {
            @Override
            public void configure() {
                from(dtaqUri+"&greedy=true")
                .process((exchange) -> {
                	int val = ctr.incrementAndGet();
                	if(val % 1000 == 0) {
                		System.out.println("processed "+val);
                	}
                })
                .convertBodyTo(String.class, "UTF-8") // We do this to convert the bytes from the data queue (UTF-8 JSON data) into a String object in the message
		.threads(5,200).maxQueueSize(Integer.MAX_VALUE)
                .to(kafkaUri)
                ; 
            }
        });
        // This actually "starts" the route, so Camel will start monitoring and routing activity here.
        context.start();

        // Since this program is designed to just run forever (until user cancel), we can just sleep the
        // main thread. Camel's work will happen in secondary threads.
        Thread.sleep(Long.MAX_VALUE);
        context.stop();
        context.close();
    }
}


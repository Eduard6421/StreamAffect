/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.mavenproject1;

import java.util.Arrays;
import javax.imageio.ImageIO;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
/**
 *
 * @author eduard
 */
public class Streaming {
    
    const String sadDirectory = "hdfs://localhost:9000/dataset/sad";
    
    public static void main(String args[]){
        
        
        SparkConf configuration = new SparkConf().setMaster("local").setAppName("Streaming App");
        JavaSparkContext sparkContext = new JavaSparkContext(configuration);
        JavaStreamingContext streamingContext = new JavaStreamingContext(sparkContext,Durations.seconds(5));
        
        JavaDStream<ImageIO> asd = streamingContext.fileStream(directory, kClass, vClass, fClass)
        
    }
    
}

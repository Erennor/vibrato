package com.example.jean.vibratohandler;

import java.io.BufferedInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Created by jean on 20/05/16.
 */
public class HTTPHandler {
    /**
     * @param param : command to be sent to server
     *              e.g. l1,my_script
     */
    public static void sendPost(final String param) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    sendPostThread(param);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }
    private static void sendPostThread(String param){

        try {
            URL url = new URL("http://192.168.132.98:8080/rest/items/VibratoListener");
            HttpURLConnection urlConnection = null;
            try {
                urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setDoOutput(true);
                urlConnection.setRequestProperty( "charset", "utf-8");
                urlConnection.setRequestMethod("POST");
                urlConnection.addRequestProperty("Content-Type","text/plain");
                DataOutputStream wr = new DataOutputStream(urlConnection.getOutputStream());
                wr.writeBytes(param);
                wr.flush();
                wr.close();
                try{
                    InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                }catch (Exception e){
                    e.printStackTrace();
                }finally {
                    urlConnection.disconnect();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
    }

    public static void main(String args[]){
        sendPost("test_send_post");
    }
}

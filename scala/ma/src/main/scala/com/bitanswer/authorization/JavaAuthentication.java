package com.bitanswer.authorization;

import com.bitanswer.library.BitAnswer;
import com.bitanswer.library.BitAnswer.BitAnswerException;

public class JavaAuthentication {
    /**
     * feature id 1 is for encryption and
     * decryption feature id 2 is for read and
     * write feature id 3 is for convert
     */
    /** The Constant DEMO_FEATURE_CRYPTO. */
    static final int    DEMO_FEATURE_CRYPTO  = 1;

    /** The Constant DEMO_FEATURE_RW. */
    static final int    DEMO_FEATURE_RW      = 2;

    /** The Constant DEMO_FEATURE_CONVERT. */
    static final int    DEMO_FEATURE_CONVERT = 3;
    // you can change sn here
    /** The Constant SERIAL_NUMBER. */
    static final String SERIAL_NUMBER = ""; // please input sn here

    public void login(String serial_number){
        boolean bLogin = false;
        BitAnswer bitAnswer = null;
        try {

            System.out.println("In the license certificate.......");

            bitAnswer = new BitAnswer();

            // login
            String sn = serial_number;
            bitAnswer.login(null, sn, BitAnswer.LoginMode.AUTO);
            bLogin = true;
            System.out.println("Login success.");

        } catch (BitAnswerException e) {
            System.out.println("error code:" + e.getErrorCode());
            e.printStackTrace();
            System.exit(1);
        } catch (Throwable e) {
            e.printStackTrace();
        }
        // Logout
        try {
            if (bLogin) {
                bitAnswer.logout();
                System.out.println("Logout success.");
                System.out.println("License has been certified successfully.");
            }
        } catch (BitAnswerException e1) {
            System.out.println(e1.getErrorCode());
            System.exit(1);
        }
    }
}


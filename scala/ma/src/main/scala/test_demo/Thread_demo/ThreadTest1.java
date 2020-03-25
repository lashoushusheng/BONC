package test_demo.Thread_demo;

class MThread implements Runnable{

    @Override
    public void run() {
        for (int i=0;i<100;i++){
            if(i%2 != 0){
                System.out.println(Thread.currentThread().getName() + ":" + i);
//                System.out.println(i);
            }
        }
    }
}

public class ThreadTest1 {
    public static void main(String[] args) {
        MThread mThread = new MThread();

        Thread t1 = new Thread(mThread);
        Thread t2 = new Thread(mThread);

        t1.start();
        t1.setName("线程1");
        t2.start();
        t2.setName("线程2");
    }
}

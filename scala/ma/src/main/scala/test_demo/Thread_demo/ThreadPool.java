package test_demo.Thread_demo;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

class NumberThread implements Runnable{
    @Override
    public void run() {
        for (int i=0;i<=100;i++){
            if(i%2 == 0){
                System.out.println(Thread.currentThread().getName() + "haohao1");
            }
        }
    }
}

class NumberThread1 implements Runnable{
    @Override
    public void run() {
//        for (int i=0;i<2;i++){
//            if(i%2 != 0){
//                System.out.println(Thread.currentThread().getName() + "haohao");
//            }
//        }
        System.out.println("haohao");
    }
}

public class ThreadPool {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService service = Executors.newFixedThreadPool(1);
        ThreadPoolExecutor service1 = (ThreadPoolExecutor)service;

//        Class<? extends ExecutorService> aClass = service.getClass();
//        System.out.println(aClass);

        NumberThread numberThread = new NumberThread();
        NumberThread1 numberThread1 = new NumberThread1();
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);
        service.execute(numberThread1);

        System.out.println(service1.getPoolSize());
//        service.submit();
        Thread.sleep(3000);
        System.out.println(service1.getPoolSize());

        service.shutdown();



    }
}

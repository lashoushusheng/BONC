package test_demo.Thread_demo;

/**
 * sold ticket
 */
class Window1 extends WindowTest1 implements Runnable{
    private int ticket = 100;
    @Override
    public void run() {
        while (true){
            if(ticket > 0){
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(Thread.currentThread().getName() + ": ticket No is: " + ticket);
                ticket--;
            }else {
                break;
            }
        }
    }
}

public class WindowTest1 {
    public static void main(String[] args) {
        Window1 w = new Window1();

        Thread t1 = new Thread(w);
        Thread t2 = new Thread(w);
        Thread t3 = new Thread(w);

        t1.setName("Number1");
        t2.setName("Number2");
        t3.setName("Number3");

        t1.start();
        t2.start();
        t3.start();

    }
}

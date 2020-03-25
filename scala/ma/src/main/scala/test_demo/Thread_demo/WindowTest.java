package test_demo.Thread_demo;

/**
 * sold ticket
 */
class Window extends Thread{
    private static int ticket = 100;
    @Override
    public void run() {
        while (true){
            if(ticket > 0){
                System.out.println(getName() + ": ticket No is: " + ticket);
                ticket--;
            }else {
                break;
            }
        }
    }
}

public class WindowTest {
    public static void main(String[] args) {
        Window t1 = new Window();
        Window t2 = new Window();
        Window t3 = new Window();

        t1.setName("window 1");
        t2.setName("window 2");
        t3.setName("window 3");

        t1.start();
        t2.start();
        t3.start();

    }
}

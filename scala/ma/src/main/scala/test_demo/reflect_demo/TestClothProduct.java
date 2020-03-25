package test_demo.reflect_demo;

interface ClothFactory{
    void productCloth();
}

// 被代理类
class NikeClothFactory implements ClothFactory{

    @Override
    public void productCloth() {
        System.out.println("耐克工厂生产一批衣服");
    }
}

// 代理类
class ProxyFactory implements ClothFactory{
    ClothFactory cf;

    public ProxyFactory(ClothFactory cf){
        this.cf = cf;
    }

    @Override
    public void productCloth() {
        System.out.println("代理类开始执行，收代理费1000");
        cf.productCloth();
    }
}


public class TestClothProduct {
}

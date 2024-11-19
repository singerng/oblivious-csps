import java.util.*;

// Code used to generate input into Python program
public class generator {
    public static void main(String[] args)  {
        // The number of classes is equal to (2 * size) + 3
        int size = 200;

        // bias = numerator / denominator
        double numerator = 1.0;
        double denominator = 2.0;


        double[] nums = new double[size + 1];
        System.out.print("print(primal_lp(2," + size + ",(");
        for(int i = 0; i <= size; i++)  {
            nums[i] = (double) ((double) (numerator*i)/(denominator*size) + (double) (numerator*(i+1))/(denominator*size))/2.0;
            System.out.print((numerator*i) + "/" + (denominator*size));
            if(i != size)  {
                System.out.print(",");
            }
        }

        System.out.print("),(");

        for(int d = 0; d < size; d++)  {
            System.out.print((nums[d] * denominator / numerator + 1.0) / 2.0 + ",");
        }
        System.out.println(")))");
    }
}
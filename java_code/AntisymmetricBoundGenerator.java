import java.util.*;
import java.io.*;

public class AntisymmetricBoundGenerator {
    public static double frac(int x)  {
        if(x / 10 == 0)  {
            return Double.parseDouble("0.0" + x);
        } else  {
            return Double.parseDouble("0." + x);
        }
    }

    public static void main(String[] args) throws IOException  {
        // Change file name here
        String fileName = "fiveclassintervalgenerated.txt";
        BufferedWriter bwriter = new BufferedWriter(new FileWriter(fileName));

        double bias = 1.0 / 3.8625;

        // Graph
        // S, N, 1 = bias a, 2 = bias b, 3 = bias 1/2, 4 = bias 1 - b, 5 = bias 1 - a

        String print = "LinearOptimization[sol,{";

        // S vertices
        for(int i = 1; i <= 5; i++)  {
            if(i == 1)  {
                print += "0(";
            } else if(i == 2)  {
                print += bias + "(";
            } else if(i == 3)  {
                print += "0.5(";
            } else if(i == 4)  {
                print += "0.5(";
            } else  {
                print += (1.0-bias) + "(";
            }

            for(int j = 1; j <= 5; j++)  {
                print += "s" + i + "s" + j + "+";
                print += "s" + i + "n" + j + "+";
                print += "s" + j + "s" + i + "+";
                print += "n" + j + "s" + i + "+";
            }

            print += "0)<=";

            for(int j = 1; j <= 5; j++)  {
                print += "s" + i + "s" + j + "+";
                print += "s" + i + "n" + j + "+";
            }

            print += "0<=";

            if(i == 1)  {
                print += bias + "(";
            } else if(i == 2)  {
                print += "0.5(";
            } else if(i == 3)  {
                print += "0.5(";
            } else if(i == 4)  {
                print += (1.0 - bias) + "(";
            } else  {
                print += "(";
            }

            for(int j = 1; j <= 5; j++)  {
                print += "s" + i + "s" + j + "+";
                print += "s" + i + "n" + j + "+";
                print += "s" + j + "s" + i + "+";
                print += "n" + j + "s" + i + "+";
            }

            print += "0),";
        }

        // N vertices
        for(int i = 1; i <= 5; i++)  {
            if(i == 1)  {
                print += "0(";
            } else if(i == 2)  {
                print += bias + "(";
            } else if(i == 3)  {
                print += "0.5(";
            } else if(i == 4)  {
                print += "0.5(";
            } else  {
                print += (1.0-bias) + "(";
            }

            for(int j = 1; j <= 5; j++)  {
                print += "n" + i + "s" + j + "+";
                print += "n" + i + "n" + j + "+";
                print += "s" + j + "n" + i + "+";
                print += "n" + j + "n" + i + "+";
            }

            print += "0)<=";

            for(int j = 1; j <= 5; j++)  {
                print += "n" + i + "s" + j + "+";
                print += "n" + i + "n" + j + "+";
            }

            print += "0<=";

            if(i == 1)  {
                print += bias + "(";
            } else if(i == 2)  {
                print += "0.5(";
            } else if(i == 3)  {
                print += "0.5(";
            } else if(i == 4)  {
                print += (1.0 - bias) + "(";
            } else  {
                print += "(";
            }

            for(int j = 1; j <= 5; j++)  {
                print += "n" + i + "s" + j + "+";
                print += "n" + i + "n" + j + "+";
                print += "s" + j + "n" + i + "+";
                print += "n" + j + "n" + i + "+";
            }

            print += "0),";
        }

        for(int i = 1; i <= 5; i++)  {
            for(int j = 1; j <= 5; j++)  {
                print += "s" + i + "n" + j + "+";
            }
        }
        print += "0==1,";

        for(int i = 1; i <= 5; i++)  {
            for(int j = 1; j <= 5; j++)  {
                print += "s" + i + "s" + j + ">=0,";
                print += "s" + i + "n" + j + ">=0,";
                print += "n" + i + "s" + j + ">=0,";
                print += "n" + i + "n" + j + ">=0,";
            }
        }

        String reqs = "";

        for(int x1 = 0; x1 <= 50; x1 += 1)  {
            for(int x2 = 0; x2 <= 50; x2 += 1)  {
                double p1 = frac(x1);
                double p2 = frac(x2);
                reqs += "sol>=";
                reqs += String.format("%.6f", (p1 * (1-p1))) + "(s1n1 + n1s1 + s5n5 + n5s5)+";
                reqs += String.format("%.6f", (p2 * (1-p2))) + "(s2n2 + n2s2 + s4n4 + n4s4)+";
                reqs += String.format("%.6f", (p1 * p1)) + "(s1s5 + s1n5 + n1s5 + n1n5)+";
                reqs += String.format("%.6f", (p2 * p2)) + "(s2s4 + s2n4 + n2s4 + n2n4)+";
                reqs += String.format("%.6f", ((1-p1) * (1-p1))) + "(s5s1 + s5n1 + n5s1 + n5n1)+";
                reqs += String.format("%.6f", ((1-p2) * (1-p2))) + "(s4s2 + s4n2 + n4s2 + n4n2)+"; // 24 vars so far
                reqs += String.format("%.6f", (p1 * 0.5)) + "(s1s3 + s1n3 + n1s3 + n1n3 + s3s5 + s3n5 + n3s5 + n3n5)+";
                reqs += String.format("%.6f", (p2 * 0.5)) + "(s2s3 + s2n3 + n2s3 + n2n3 + s3s4 + s3n4 + n3s4 + n3n4)+"; // 40 vars so far
                reqs += String.format("%.6f", ((1-p1) * 0.5)) + "(s5s3 + s5n3 + n5s3 + n5n3 + s3s1 + s3n1 + n3s1 + n3n1)+";
                reqs += String.format("%.6f", ((1-p2) * 0.5)) + "(s4s3 + s4n3 + n4s3 + n4n3 + s3s2 + s3n2 + n3s2 + n3n2)+";
                reqs += String.format("%.6f", (p1 * p2)) + "(s1s4 + s1n4 + n1s4 + n1n4 + s2s5 + s2n5 + n2s5 + n2n5)+"; // 64 vars so far
                reqs += String.format("%.6f", (p1 * (1-p2))) + "(s1s2 + s1n2 + n1s2 + n1n2 + s4s5 + s4n5 + n4s5 + n4n5)+";
                reqs += String.format("%.6f", ((1-p1) * p2)) + "(s5s4 + s5n4 + n5s4 + n5n4 + s2s1 + s2n1 + n2s1 + n2n1)+"; // 80 vars so far
                reqs += String.format("%.6f", ((1-p1) * (1-p2))) + "(s5s2 + s5n2 + n5s2 + n5n2 + s4s1 + s4n1 + n4s1 + n4n1)+"; // 88 vars so far
                reqs += 0.25 + "(s3n3 + n3s3),"; // 90 vars so far, good
                print += reqs;
                reqs = "";
            }
        }

        print += "s1s1==0,n1n1==0,s2s2==0,n2n2==0,s3s3==0,n3n3==0,s4s4==0,n4n4==0,s5s5==0,n5n5==0},{";

        for(int i = 1; i <= 5; i++)  {
            for(int j = 1; j <= 5; j++)  {
                print += "s" + i + "s" + j + ",";
                print += "s" + i + "n" + j + ",";
                print += "n" + i + "s" + j + ",";
                print += "n" + i + "n" + j + ",";
            }
        }

        print += "sol}]";

        bwriter.write(print + "\r\n");
        bwriter.close();
    }
}
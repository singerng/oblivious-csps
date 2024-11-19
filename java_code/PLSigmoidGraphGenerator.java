import java.util.*;
import java.awt.datatransfer.StringSelection;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.io.*;

// This generated the graph for the Theorem to prove the bound on PL Sigmoid Functions
// The output of this is plugged into Mathematica to get the graph.

public class PLSigmoidGraphGenerator {
    public static void main(String[] args) throws IOException {
        final int numMidClasses = 20;
        final double smallerBoundary = 1.0 / 3.8625;

        BufferedWriter bwriter = new BufferedWriter(new FileWriter("singlelpnoninterval.txt"));

        int numClasses = numMidClasses + 2;
        double[] boundaries = new double[numMidClasses+3];
        for(int i = 0; i <= numMidClasses; i++)  {
            boundaries[i + 1] = 0.25 + i * (0.5 / (double) numMidClasses);
        }

        boundaries[0] = 0;
        boundaries[numMidClasses + 2] = 1;

        String oneSumReq = "";
        String positiveReq = "";
        for(int i = 0; i < numClasses; i++)  {
            for(int j = 0; j < numClasses; j++)  {
                oneSumReq += "c" + i + "n" + j + "+";
                positiveReq += "c" + i + "c" + j + ">=0,";
                positiveReq += "c" + i + "n" + j + ">=0,";
                positiveReq += "n" + i + "c" + j + ">=0,";
                positiveReq += "n" + i + "n" + j + ">=0,";
            }
        }
        oneSumReq = oneSumReq.substring(0, oneSumReq.length() - 1) + "==1,";

        String boundaryReq = "";

        for(int i = 0; i < numClasses; i++)  {
            boundaryReq += ((boundaries[i] + boundaries[i + 1]) / 2.0) + "(";
            for(int j = 0; j < numClasses; j++)  {
                boundaryReq += "c" + i + "c" + j + "+c" + j + "c" + i + "+";
                boundaryReq += "c" + i + "n" + j + "+n" + j + "c" + i + "+";
            }

            boundaryReq += "0)==";

            for(int j = 0; j < numClasses; j++)  {
                boundaryReq += "c" + i + "c" + j + "+";
                boundaryReq += "c" + i + "n" + j + "+";
            }

            boundaryReq += "0,";


            // Now do it with n

            boundaryReq += (boundaries[i] + boundaries[i + 1]) / 2.0 + "(";
            for(int j = 0; j < numClasses; j++)  {
                boundaryReq += "n" + i + "c" + j + "+c" + j + "n" + i + "+";
                boundaryReq += "n" + i + "n" + j + "+n" + j + "n" + i + "+";
            }

            boundaryReq += "0)==";

            for(int j = 0; j < numClasses; j++)  {
                boundaryReq += "n" + i + "c" + j + "+";
                boundaryReq += "n" + i + "n" + j + "+";
            }

            boundaryReq += "0,";
        }

        String solReq = "sol>=";
        double[] midPoints = new double[numClasses];

        for(int i = 0; i < numClasses; i++)  {
            midPoints[i] = (boundaries[i] + boundaries[i + 1]) / 2.0;
            System.out.println(midPoints[i]);
        }

        for(int i = 0; i < numClasses; i++)  {
            for(int j = 0; j < numClasses; j++)  {
                if(midPoints[i] <= smallerBoundary)  {
                    continue;
                } else if(midPoints[i] >= 1.0 - smallerBoundary)  {
                    solReq += "1*";
                } else  {
                    solReq += (1.0 / (1.0 - 2.0 * smallerBoundary) * (midPoints[i] - smallerBoundary)) + "*";
                    if((1.0 / (1.0 - 2.0 * smallerBoundary) * (midPoints[i] - smallerBoundary)) < 0.0) System.out.println("NO " + midPoints[i]);
                }

                if(midPoints[j] <= smallerBoundary)  {
                    
                } else if(midPoints[j] >= 1.0 - smallerBoundary)  {
                    solReq += "0+";
                    continue;
                } else  {
                    solReq += (1.0 - (1.0 / (1.0 - 2.0 * smallerBoundary) * (midPoints[j] - smallerBoundary))) + "*";
                    if((1.0 - (1.0 / (1.0 - 2.0 * smallerBoundary) * (midPoints[j] - smallerBoundary))) < 0.0) System.out.println("NO2 " + midPoints[j]);
                }

                solReq += "(c" + i + "c" + j + "+c" + i + "n" + j + "+n" + i + "c" + j + "+n" + i + "n" + j + ")+";
            }
        }

        solReq = solReq.substring(0, solReq.length() - 1);

        //System.out.println(solReq + "\n");

        StringSelection stringSelection = new StringSelection(oneSumReq + positiveReq + boundaryReq + solReq);
        Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
        clipboard.setContents(stringSelection, null);

        String variables = "sol";
        for(int i = 0; i < numClasses; i++)  {
            for(int j = 0; j < numClasses; j++)  {
                variables += "," + "c" + i + "c" + j + "," + "c" + i + "n" + j + "," + "n" + i + "c" + j + "," + "n" + i + "n" + j;
            }
        }

        bwriter.write("LinearOptimization[sol,{" + oneSumReq + positiveReq + boundaryReq + solReq + "},{" + variables + "}]\r\n");
        bwriter.close();
    }
}
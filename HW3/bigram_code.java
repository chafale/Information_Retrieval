import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.util.HashMap;
import java.util.HashSet;

public class BigramInvertedIndex {
  public static class TokenizerMapper extends Mapper<Object, Text, Text, Text> {
    private Text bigrams = new Text();
    private Text documentID = new Text();
    HashSet<String> bigramSet = new HashSet<String>();

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      bigramSet.add("computer science");
      bigramSet.add("information retrieval");
      bigramSet.add("power politics");
      bigramSet.add("los angeles");
      bigramSet.add("bruce willis");

      String[] document = value.toString().split("\t", 2);
      String text = document[1].toLowerCase();
      text = text.replaceAll("[^a-z\\s]", " ");
      text = text.replaceAll("\\s+", " ");

      documentID.set(document[0]);

      StringTokenizer tokenizer = new StringTokenizer(text);
      String previous = tokenizer.nextToken();
      while (tokenizer.hasMoreTokens()) {
        String current = tokenizer.nextToken();
        String bigramString = previous + " " + current;
        if (bigramSet.contains(bigramString)) {
          bigrams.set(bigramString);
          context.write(bigrams, documentID);
        }
        previous = current;
      }
    }
  }

  public static class IndexReducer extends Reducer<Text, Text, Text, Text> {
    private Text result = new Text();

    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      HashMap<String, Integer> count = new HashMap<>();
      for (Text val : values) {
        String documentID = val.toString();
        count.put(documentID, count.getOrDefault(documentID, 0) + 1);
      }

      StringBuilder s = new StringBuilder();
      for (String k : count.keySet())
        s.append(k).append(":").append(count.get(k)).append("\t");

      result.set(s.substring(0, s.length() - 1));
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "BigramInvertedIndex");
    job.setJarByClass(BigramInvertedIndex.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setReducerClass(IndexReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
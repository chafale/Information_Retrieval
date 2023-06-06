import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;


public class Controller {
    public static void main(String[] args) throws Exception {
        CrawlConfig config = new CrawlConfig();

        /*
        Setup configuration
         */
        int numberOfCrawlers = 16;
        String crawlStorageFolder = "data/crawl";
        config.setCrawlStorageFolder(crawlStorageFolder);
        config.setIncludeBinaryContentInCrawling(true);
        config.setMaxDepthOfCrawling(16);
        config.setMaxPagesToFetch(20000);
        config.setPolitenessDelay(500);
        config.setUserAgentString("Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        );

        /*
         * Instantiate the controller for this crawl.
         */
        PageFetcher pageFetcher = new PageFetcher(config);
        RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
        RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
        CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);

        /*
         * Seed URL's
         */
        controller.addSeed("https://www.wsj.com");

        /*
         * Start the crawl
         */
        controller.start(BasicCrawler.class, numberOfCrawlers);

        StringBuilder output_1 = new StringBuilder("URL,Status\n");
        StringBuilder output_2 = new StringBuilder("URL,Size,Outgoing Links,Content Type\n");
        StringBuilder output_3 = new StringBuilder("URL,Status\n");

        for (Object t : controller.getCrawlersLocalData()) {
            String[] tasks = (String[]) t;
            output_1.append(tasks[0]);
            output_2.append(tasks[1]);
            output_3.append(tasks[2]);
        }

        createCSV(output_1, "crawler_stats/fetch_wsj.csv");
        createCSV(output_2, "crawler_stats/visit_wsj.csv");
        createCSV(output_3, "crawler_stats/urls_wsj.csv");
    }

    private static void createCSV(StringBuilder output, String s) throws IOException {
        PrintWriter writer = new PrintWriter(s, String.valueOf(StandardCharsets.UTF_8));
        writer.println(output.toString().trim());
        writer.flush();
        writer.close();
    }
}
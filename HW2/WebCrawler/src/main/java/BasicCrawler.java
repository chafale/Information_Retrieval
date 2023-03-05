import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;

public class BasicCrawler extends WebCrawler {
    private final static Pattern FILTERS = Pattern.compile(
            ".*(\\.(" + "css|js|json|webmanifest|ttf|svg|wav|avi|mov|mpeg" +
                    "|mpg|ram|m4v|wma|wmv|mid|txt|mp2|mp3|mp4|zip|rar|gz|exe|ico))$");

    private String fetch_task = "";
    private String visited_task = "";
    private String urls_task = "";
    private final HashSet<String> visited = new HashSet<>();

    @Override
    public Object getMyLocalData() {
        return new String[]{fetch_task, visited_task, urls_task};
    }

    @Override
    protected void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {
        String url = webUrl.getURL().toLowerCase().replaceAll(",", "_");
        fetch_task += url + "," + statusCode + "\n";
        visited.add(url);
    }

    @Override
    public boolean shouldVisit(Page referringPage, WebURL url) {
        String href = url.getURL().toLowerCase().replaceAll(",", "_");
        boolean isValid = href.startsWith("http://www.wsj.com/") || href.startsWith("https://www.wsj.com/");
        if (isValid) {
            urls_task += href + ",OK\n";
        }
        else {
            urls_task += href + ",N_OK\n";
        }
        boolean hasNotSeen = !visited.contains(href);
        return !FILTERS.matcher(href).matches() && isValid && hasNotSeen;
    }

    @Override
    public void visit(Page page) {
        int docid = page.getWebURL().getDocid();
        System.out.println("Docid: " + docid);
        System.out.println("\n==========================\n");

        String url = page.getWebURL().getURL().toLowerCase().replaceAll(",", "_");
        int numberOfOutLinks = 0;
        int fileSize = page.getContentData().length;
        String contentType = page.getContentType().split(";")[0];

        boolean isCorrectType = contentType.contains("html") | contentType.contains("image") |
                contentType.contains("doc") | contentType.contains("pdf");
        if (!isCorrectType)
            return;

        if (page.getParseData() instanceof HtmlParseData) {
            HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
            Set<WebURL> links = htmlParseData.getOutgoingUrls();
            numberOfOutLinks += links.size();
        }

        visited_task += url + "," + fileSize + "," + numberOfOutLinks + "," + contentType + "\n";
    }
}
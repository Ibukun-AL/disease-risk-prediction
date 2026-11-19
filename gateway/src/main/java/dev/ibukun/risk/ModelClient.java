package dev.ibukun.risk;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.ClientHttpRequestFactories;
import org.springframework.boot.web.client.ClientHttpRequestFactorySettings;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class ModelClient {
  public record Result(double risk, String label) {}

  private final RestClient client;

  public ModelClient(@Value("${model.url}") String baseUrl) {
    var settings = ClientHttpRequestFactorySettings.DEFAULTS
        .withConnectTimeout(Duration.ofSeconds(2))
        .withReadTimeout(Duration.ofSeconds(2));
    this.client = RestClient.builder()
        .baseUrl(baseUrl)
        .requestFactory(ClientHttpRequestFactories.get(settings))
        .build();
  }

  public Result predict(List<Double> features) {
    try {
      return client.post().uri("/predict").body(Map.of("features", features)).retrieve().body(Result.class);
    } catch (Exception e) {
      throw new ModelUnavailableException(e);
    }
  }
}

package dev.ibukun.risk;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.not;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.io.IOException;
import java.util.Collections;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class RiskControllerTest {
  static MockWebServer model = new MockWebServer();

  @BeforeAll
  static void start() throws IOException {
    model.start();
  }

  @AfterAll
  static void stop() throws IOException {
    model.shutdown();
  }

  @DynamicPropertySource
  static void props(DynamicPropertyRegistry r) {
    r.add("model.url", () -> "http://localhost:" + model.getPort());
  }

  @Autowired MockMvc mvc;

  static String body(int n) {
    return "{\"features\":" + Collections.nCopies(n, 1.5) + "}";
  }

  @Test
  @Order(1)
  void returnsRiskForValidVector() throws Exception {
    model.enqueue(new MockResponse().setHeader("Content-Type", "application/json").setBody("{\"risk\":0.82,\"label\":\"higher\"}"));
    mvc.perform(post("/api/v1/risk").contentType(MediaType.APPLICATION_JSON).content(body(30)))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.risk").value(0.82))
        .andExpect(jsonPath("$.label").value("higher"))
        .andExpect(jsonPath("$.disclaimer").value("Not medical advice. Demonstration on a public dataset."));
  }

  @Test
  @Order(2)
  void rejectsWrongLength400() throws Exception {
    mvc.perform(post("/api/v1/risk").contentType(MediaType.APPLICATION_JSON).content(body(29)))
        .andExpect(status().isBadRequest());
  }

  @Test
  @Order(3)
  void returns503WhenModelDown() throws Exception {
    model.shutdown();
    mvc.perform(post("/api/v1/risk").contentType(MediaType.APPLICATION_JSON).content(body(30)))
        .andExpect(status().isServiceUnavailable())
        .andExpect(jsonPath("$.error").value("model service unavailable"))
        .andExpect(content().string(not(containsString("Exception"))));
  }
}

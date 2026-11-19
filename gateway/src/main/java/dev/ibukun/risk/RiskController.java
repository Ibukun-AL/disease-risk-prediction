package dev.ibukun.risk;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class RiskController {
  static final String DISCLAIMER = "Not medical advice. Demonstration on a public dataset.";
  private final ModelClient model;

  public RiskController(ModelClient model) {
    this.model = model;
  }

  @PostMapping("/risk")
  public RiskResponse risk(@Valid @RequestBody RiskRequest request) {
    var r = model.predict(request.features());
    return new RiskResponse(r.risk(), r.label(), DISCLAIMER);
  }
}

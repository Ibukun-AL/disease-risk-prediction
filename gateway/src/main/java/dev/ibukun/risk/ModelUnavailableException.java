package dev.ibukun.risk;

public class ModelUnavailableException extends RuntimeException {
  public ModelUnavailableException(Throwable cause) {
    super("model service unavailable", cause);
  }
}

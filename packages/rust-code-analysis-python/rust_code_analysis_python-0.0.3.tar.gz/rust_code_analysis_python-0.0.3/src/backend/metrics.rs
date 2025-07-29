use std::path::PathBuf;

use rust_code_analysis::{Callback, FuncSpace, ParserTrait, action, guess_language, metrics};

/// Payload containing source code used to compute metrics.
#[derive(Debug)]
pub struct MetricsPayload {
    /// Source code filename.
    pub file_name: String,
    /// Source code used to compute metrics.
    pub code: String,
    /// Flag to consider only unit space metrics.
    pub unit: bool,
}

/// Server response containing metrics for every space present in
/// the requested source code.
pub type MetricsResponse = Result<FuncSpace, String>;

/// Server request configuration.
#[derive(Debug)]
pub struct MetricsCfg {
    /// Path to the source file.
    pub path: PathBuf,
    /// Flag to consider only unit space metrics.
    pub unit: bool,
}

/// Unit structure to implement the `Callback` trait.
pub struct MetricsCallback;

impl Callback for MetricsCallback {
    type Res = MetricsResponse;
    type Cfg = MetricsCfg;

    fn call<T: ParserTrait>(cfg: Self::Cfg, parser: &T) -> Self::Res {
        let spaces = metrics(parser, &cfg.path);
        let spaces = if cfg.unit {
            if let Some(mut spaces) = spaces {
                spaces.spaces.clear();
                Some(spaces)
            } else {
                None
            }
        } else {
            spaces
        };
        spaces.ok_or("Failed to compute metrics".to_string())
    }
}

pub fn metrics_rust(payload: MetricsPayload) -> MetricsResponse {
    let path = PathBuf::from(&payload.file_name);
    let buf = payload.code.into_bytes();
    let (language, _name) = guess_language(&buf, &path);
    if let Some(language) = language {
        let cfg = MetricsCfg {
            path,
            unit: payload.unit,
        };
        action::<MetricsCallback>(&language, buf, &PathBuf::from(""), None, cfg)
    } else {
        Err("The file extension doesn't correspond to a valid language".to_string())
    }
}

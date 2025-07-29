use rust_code_analysis::{Callback, LANG, ParserTrait, action, guess_language, rm_comments};
use std::path::PathBuf;

/// Payload containing source code with comments to be removed.
#[derive(Debug)]
pub struct CommentRemovalPayload {
    /// Source code filename.
    pub file_name: String,
    /// Source code with comments to be removed.
    pub code: String,
}

pub type CommentRemovalResponse = Result<String, String>;

/// Unit structure to implement the `Callback` trait.
#[derive(Debug)]
pub struct CommentRemovalCallback;

impl Callback for CommentRemovalCallback {
    type Res = String;
    type Cfg = ();

    fn call<T: ParserTrait>(_cfg: Self::Cfg, parser: &T) -> Self::Res {
        // rm_comments returns None iff no comments were found
        let code = rm_comments(parser).unwrap_or_else(|| parser.get_code().to_vec());
        String::from_utf8_lossy(&code).into_owned()
    }
}

pub fn comment_removal_rust(payload: CommentRemovalPayload) -> CommentRemovalResponse {
    let path = PathBuf::from(payload.file_name);
    let buf = payload.code.into_bytes();
    let (language, _) = guess_language(&buf, path);
    if let Some(language) = language {
        let language = if language == LANG::Cpp {
            LANG::Ccomment
        } else {
            language
        };
        let result = action::<CommentRemovalCallback>(&language, buf, &PathBuf::from(""), None, ());
        Ok(result)
    } else {
        Err("The file extension doesn't correspond to a valid language".to_string())
    }
}

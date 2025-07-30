use noodles::sam::alignment::record_buf::Cigar;
use noodles::sam::alignment::{
    record::cigar::op::Kind, record::cigar::Op, record::data::field::Tag,
    record_buf::data::field::Value,
};

use anyhow::Context;
use pyo3::prelude::*;
use pyo3::types::PyAny;

/// Python 用に限定した「オーバーライド」構造体
#[pyclass]
#[derive(Clone)]
pub struct RecordOverride {
    pub reference_sequence_id: Option<u32>,
    pub cigar: Option<Cigar>,
    pub alignment_start: Option<u32>,
    pub tags: Vec<(Tag, Value)>,
}

#[pymethods]
impl RecordOverride {
    #[new]
    fn new(
        reference_sequence_id: Option<u32>,
        cigar: Option<Vec<(u32, u32)>>,
        alignment_start: Option<u32>,
        tags: Option<Vec<(String, Py<PyAny>)>>,
    ) -> Self {
        let cigar_opt = match cigar {
            Some(cigar_list) => convert_vec_to_cigar(cigar_list).ok(),
            None => None,
        };

        let mut tag_vec = Vec::new();
        if let Some(tag_list) = tags {
            for (k, v_any) in tag_list {
                if let (Ok(tag), Ok(val)) =
                    (convert_string_to_tag(k), convert_pyany_to_value(v_any))
                {
                    tag_vec.push((tag, val));
                }
            }
        }

        RecordOverride {
            reference_sequence_id,
            cigar: cigar_opt,
            alignment_start: alignment_start,
            tags: tag_vec,
        }
    }

    /// override する reference_sequence_id (None なら元値を使う)
    #[setter]
    fn reference_sequence_id(&mut self, rid: u32) {
        self.reference_sequence_id = Some(rid);
    }

    #[setter]
    fn alignment_start(&mut self, pos: u32) {
        self.alignment_start = Some(pos);
    }

    #[setter]
    fn cigar(&mut self, cigar_list: Vec<(u32, u32)>) {
        // CIGAR の変換
        let cigar = convert_vec_to_cigar(cigar_list).unwrap();
        self.cigar = Some(cigar);
    }

    /// 追加タグ: Python からは List[(str, Any)] を受け取る
    #[setter]
    fn tags(&mut self, vals: Vec<(String, Py<PyAny>)>) {
        for (k, v_any) in vals {
            let tag = convert_string_to_tag(k).expect("Invalid tag");
            let val = convert_pyany_to_value(v_any).expect("Invalid value");
            self.tags.push((tag, val));
        }
    }
}

fn convert_string_to_tag(tag_str: String) -> anyhow::Result<Tag> {
    if tag_str.len() != 2 {
        return Err(anyhow::anyhow!("Invalid tag length: {}", tag_str.len()));
    }
    let tag_bytes = tag_str.as_bytes();
    let tag = Tag::try_from([tag_bytes[0], tag_bytes[1]])
        .map_err(|_| anyhow::anyhow!("Invalid tag bytes: {} {}", tag_bytes[0], tag_bytes[1]))?;
    Ok(tag)
}

pub fn convert_pyany_to_value(obj: PyObject) -> anyhow::Result<Value> {
    Python::with_gil(|py| {
        let any = obj.into_bound(py);
        if let Ok(i) = any.extract::<i64>() {
            // ← PyAnyMethods::extract :contentReference[oaicite:2]{index=2}
            return Ok(Value::try_from(i).context(format!("failed to convert Python int `{}`", i))?);
        }

        if let Ok(i) = any.extract::<i32>() {
            // ← PyAnyMethods::extract :contentReference[oaicite:2]{index=2}
            return Ok(Value::try_from(i).context(format!("failed to convert Python int `{}`", i))?);
        }

        if let Ok(i) = any.extract::<i16>() {
            // ← PyAnyMethods::extract :contentReference[oaicite:2]{index=2}
            return Ok(Value::try_from(i).context(format!("failed to convert Python int `{}`", i))?);
        }

        if let Ok(i) = any.extract::<i8>() {
            // ← PyAnyMethods::extract :contentReference[oaicite:2]{index=2}
            return Ok(Value::try_from(i).context(format!("failed to convert Python int `{}`", i))?);
        }

        if let Ok(i) = any.extract::<u32>() {
            // ← PyAnyMethods::extract :contentReference[oaicite:2]{index=2}
            return Ok(Value::try_from(i).context(format!("failed to convert Python int `{}`", i))?);
        }

        if let Ok(i) = any.extract::<u16>() {
            // ← PyAnyMethods::extract :contentReference[oaicite:2]{index=2}
            return Ok(Value::try_from(i).context(format!("failed to convert Python int `{}`", i))?);
        }

        if let Ok(i) = any.extract::<u8>() {
            // ← PyAnyMethods::extract :contentReference[oaicite:2]{index=2}
            return Ok(Value::try_from(i).context(format!("failed to convert Python int `{}`", i))?);
        }

        if let Ok(f) = any.extract::<f64>() {
            return Ok(Value::from(f as f32));
        }

        if let Ok(s) = any.extract::<String>() {
            return Ok(Value::from(s.as_str()));
        }
        // その他はエラー
        let ty = any.get_type().name()?; // ← PyAnyMethods::get_type :contentReference[oaicite:3]{index=3}
        anyhow::bail!("unsupported Python type for Value: {}", ty);
    })
}

fn convert_vec_to_cigar(cigar_list: Vec<(u32, u32)>) -> anyhow::Result<Cigar> {
    let ops: Vec<Op> = cigar_list
        .into_iter()
        .map(|(k, l)| {
            let kind = match k {
                0 => Kind::Match,
                1 => Kind::SequenceMismatch,
                2 => Kind::Insertion,
                3 => Kind::Deletion,
                4 => Kind::Skip,
                5 => Kind::SoftClip,
                6 => Kind::HardClip,
                _ => return Err(anyhow::anyhow!("Invalid CIGAR operation: {}", k)),
            };
            Ok(Op::new(kind, l as usize))
        })
        .collect::<Result<_, _>>()?;
    Ok(Cigar::from(ops))
}

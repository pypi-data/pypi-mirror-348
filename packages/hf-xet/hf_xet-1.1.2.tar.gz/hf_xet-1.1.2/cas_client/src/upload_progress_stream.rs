use std::pin::Pin;
use std::task::{Context, Poll};

use bytes::Bytes;
use futures::Stream;
use more_asserts::*;

pub struct UploadProgressStream<F>
where
    F: FnMut(u64) + Send + 'static,
{
    data: Bytes,
    block_size: usize,
    progress_callback: F,
    bytes_sent: usize,
    last_update: usize,
}

impl<F> Stream for UploadProgressStream<F>
where
    F: FnMut(u64) + Send + Unpin + 'static,
{
    type Item = std::result::Result<Bytes, std::io::Error>;

    // Send the next block of data; also update the
    fn poll_next(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        debug_assert_le!(self.bytes_sent, self.data.len());

        if self.bytes_sent == self.data.len() {
            return Poll::Ready(None);
        }

        // First, see if we need to send off a progress report -- we assume that when this method is called,
        // the previous data has
        // successfully completed uploading.

        if self.last_update != 0 {
            let update = self.last_update;
            (self.progress_callback)(update as u64);
        }

        let slice_start = self.bytes_sent;
        let slice_end = (self.bytes_sent + self.block_size).min(self.data.len());

        self.last_update = slice_end - slice_start;
        self.bytes_sent = slice_end;

        Poll::Ready(Some(Ok(self.data.slice(slice_start..slice_end))))
    }
}

impl<F> UploadProgressStream<F>
where
    F: FnMut(u64) + Send + 'static,
{
    pub fn new(data: impl Into<Bytes>, block_size: usize, progress_callback: F) -> Self {
        Self {
            data: data.into(),
            block_size,
            progress_callback,
            bytes_sent: 0,
            last_update: 0,
        }
    }
}

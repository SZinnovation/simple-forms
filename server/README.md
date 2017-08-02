# A server for simple-forms

After some thinking, I'm realizing that I really don't need virtualization. For
development, I can just use morepath directly, and in production, if necessary,
I can put the server behind nginx (but that's probably not necessary.

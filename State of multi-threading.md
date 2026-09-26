# GIL

Global Interpreter Lock ( GIL ) is the lock that python interpreter itself uses when
running each instruction sequentially.

Note that an instruction does not map to each line of code. Something as complicated
as a list comprehension of a function call obviously needs dozens of instructions at
interpreter level.

## So do I need locking still?

Very much so as if I plan to rely only on GIL for my "thread" safety then I must ensure
each operation is atomic at the interpreter level.

Some are and some are not. For example something like a list append is GIL atomic,
as in it's one instruction that is run with lock held.

But a line of code is not atomic ofcourse, so this for example `arr[i] = arr[i] + 1`.
In between the individual interpreter level load store operations, the control may switch
to another thread.

So the same locking logic as any other language like cpp would've needed is also needed
here.

## The threads I make, are those real or js like event loop?

Something like `threading.Thread(target=worker)` is very much a real thread and
the OS scheduler does know about it. GIL of course serialises them so there is no real
parallel work being done.

## Is there 0 parallelisation then?

Something like NumPy can very much execute it's C level code in parallel.
At many IO blocking operations like sleep or file read or some network request,
that get blocked on OS level / native code, python releases GIL to let some other
thread's python bytecode run.

## What's the deal with asyncio?

This is what is closer to js's event loop and how a single OS thread can run multiple
co-routines through that event loop. The whole idea is co-operative control yield
when an application knows it to wait for something IO bound which is delegated to native
code. It must KNOW the mechanics of relinquishing control back to the event loop, as
the event loop is just another "function" ( sort of but it is understood by the
language itself and handled at the language level given the keywords it adds ).

### What really is a coroutine?

A coroutine is a computation that can suspend itself and later resume from where it left
off, retaining its local state.

Co-routines tie directly with an Event Loop. An event loop is a scheduler that runs coroutines.
If the computation unit ( coroutine ) does not understand yielding control ( for only the
unit knows when it is okay to do so, then there is no event loop at all ).

`await` is what is used for the actual suspend coroutine. Any `async` func is a coroutine
function, wehn you call it you get a `coroutine object`.
_except_ when the async function uses yield, in which case it's an async generator function.

## Python 3.14 and end of GIL-era

My distro and the default python it ships still uses GIL-enabled builds but the idea is that
with python 3.14, it's possible to get builds that are GIL-free and this is "officially"
supported as opposed to something experimental.

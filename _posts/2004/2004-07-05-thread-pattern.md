---
title: "Mini-Pattern: Object Method to Separate Thread"
date: 2004-07-05
layout: post
---

If you have a method on an object that doesn't return and that takes a long
time to complete then you can use this pattern to spin it off into an
unmonitored thread.


I'm going to use `medusa_http.QuixoteHandler.continue_request` as
an example.  This function doesn't return a value, instead it manipulates some
instance variables and calls methods on its own object, which makes it perfect
for this.


Move the `continue_request` function above the class definition of
`QuixoteHandler` then outdent(!) it one level. Where `continue_request` used to
be, add the function:

```python
def continue_request(self, body, request):
    import thread
    thread.start_new_thread(continue_request, (self, body, request))
```

This takes advantage of the fact that `self` has no special meaning
in Python, and the function `continue_request` can still
use it, even if it is passed from the method
`continue_request`'s instance.

I'm aware that having `self` as a variable name in a function is
potentially misleading, but this is a pretty nifty shortcut IMHO. An even
shorter and more obfuscated shortcut could be:

```python
def continue_request(*args):
    __import__('thread').start_new_thread(continue_request, args)
```

Or, for the Python 2.3 users, how about:

```python
def make_thread_method(function_name, instance):
    import new
    f = globals()[function_name]
    def tmp(*args):
        __import__('thread').start_new_thread(f, args)
    i = new.instancemethod(tmp, instance, instance.__class__)
    setattr(instance, function_name, i)

# [...]

    def __init__ (self, publisher, server_name, server):
        [...]
        make_thread_method('continue_request', self)
```

I wish Python had macros.

By the way, the `medusa_thread_http` module is hopelessly optimistic, and
probably shouldn't be used for a real deployment.


*Update*: After reading <a href="http://www.livejournal.com/users/benlast/">Ben
Last</a>'s blog and seeing a link to <a
href="http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/286185">this
recipe</a>, I can remove `self` from the parameters!

```python
def make_thread_method(function_name):
    import sys
    import new
    instance = sys._getframe(1).f_locals['self']
    f = globals()[function_name]
    def tmp(*args):
        __import__('thread').start_new_thread(f, args)
    i = new.instancemethod(tmp, instance, instance.__class__)
    setattr(instance, function_name, i)

# [...]

    def __init__ (self, publisher, server_name, server):
        [...]
        make_thread_method('continue_request')</code></pre>
```

*2nd Update*: Okay, after more tinkering and taking advantage of my <a
href="http://www.pythonware.com/daily/">Daily Python URL</a> temporary fame, I
have the below:

```python
def threadmethod(f, i=None):
    import new
    import sys
    if not i:
        i = sys._getframe(1).f_locals['self']
    def tmp(*args):
        __import__('thread').start_new_thread(f, args)
    return new.instancemethod(tmp, i, i.__class__)

class A:
    def do_thing(self):
        import time
        time.sleep(5)
        print "Wootle"
    do_thing = staticmethod(do_thing)
    def __init__(self):
        self.do_thing = threadmethod(self.do_thing)

a = A()

a.do_thing()
```

My question is: how can I make the line inside `__init__` more like
`staticmethod` (or can I?). Ideally what I want is:

```python
class A:
[...]
    do_thing = staticmethod(do_thing)
    do_thing = threadmethod(do_thing)
```

*3rd Update*: <a
href="mailto:daniel@brodienet.com">Daniel Brodie</a> writes with this even
simpler version. I can't believe I missed this- I was so busy with the idea of
converting an instance method to a static method and then back again, I didn't
see that you don't need to convert it at all!

```python
def threadmethod(func):
    def temp(*args):
        import thread
        print thread.start_new_thread(func, args)
    return temp

class A:
    def do_thing(self, some_val):
        print 'do_thing:', self, some_val
    do_thing = threadmethod(do_thing)

if __name__=='__main__':
    a = A()
    a.do_thing(5)
    while 1:
        pass #To let the thread finish up
```

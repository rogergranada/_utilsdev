#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
Dependencies: Pyjnius
----------------------

Pyjnius is a Python library for accessing Java classes. Before installing, you need the Java 
JDK and JRE installed (openjdk will do), and Cython. After installing JDK and JRE, add 
`libjvm.so` path to the `LD_LIBRARY_PATH` and set `JAVA_HOME` as:

```
export JAVA_HOME=<jdk-install-dir>
export PATH=$JAVA_HOME/bin:$PATH
export LD_LIBRARY_PATH="$JAVA_HOME:$JAVA_HOME/jre/lib/amd64/server/"
```

If using Anaconda, just type:

```
conda install -c srikanthnagella pyjnius=1.4
```

If using PIP, type:

```
pip install jnius
```

First create a Java class (MyClass.java), then transform it into a .class and .jar using:

```
javac -d . MyClass.java
jar cvf MyClass.jar MyClass.class
```

Having .jar file in the same folder of this file, you can call the python as

```
python java_in_python.py
```

"""
import jnius
import os
from os.path import realpath

JAR_FILE = realpath("MyClass.jar")
os.environ['CLASSPATH'] = JAR_FILE

class JavaParser(object):

    def __init__(self, some_name):
        myclass = jnius.autoclass('MyClass')
        self.person = myclass(some_name)

    def set_name(self, new_name):
        self.person.setName(new_name)

    def get_name(self):
        return self.person.getName()

    def set_age(self, new_age):
        self.person.setAge(new_age)

    def get_age(self):
        return self.person.getAge()


if __name__== "__main__":
    person1 = JavaParser('Person')
    person1.set_age(20)
    print('Name: '+person1.get_name())
    print('Age: '+str(person1.get_age()))

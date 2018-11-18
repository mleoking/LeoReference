## Notes
* Use ProGuard in Maven

```xml
    <build>
        <plugins>
            <plugin>
                <groupId>com.github.wvengen</groupId>
                <artifactId>proguard-maven-plugin</artifactId>
                <version>2.0.14</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>proguard</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <options>
                        <option>-ignorewarnings</option>
                        <option>-keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod</option>
                        <option>-dontshrink</option>
                        <option>-dontoptimize</option>
                        <!--<option>-dontpreverify</option>--><!-- preverification is needed for Java versions 7+, thus you also need to disable this option -->
                        <!--<option>-keep class com.abc.**</option>-->
                        <option>-keepclasseswithmembers class * {void main(...);}</option>
                        <option>-keepclassmembers class * { ** MODULE$; }</option>
                        <option>-keepclasseswithmembers class * implements scala.Product {*;}</option><!-- keep scala case class names -->
                    </options>
                    <obfuscate>true</obfuscate>
                    <injar>${project.artifactId}-${project.version}-jar-with-dependencies.jar</injar>
                    <outjar>${project.artifactId}-${project.version}-jar-with-dependencies-min.jar</outjar>
                    <outputDirectory>${project.build.directory}</outputDirectory>
                    <proguardInclude>${basedir}/proguard.conf</proguardInclude>
                    <libs>
                        <lib>${java.home}/lib/rt.jar</lib>
                        <lib>${java.home}/lib/jsse.jar</lib>
                    </libs>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

## Userful plugins
* [proguard-maven-plugin](http://wvengen.github.io/proguard-maven-plugin/)

## Q&A
* __What is the execution order of Maven plugin in same phase:__ Since Maven 3.0.3, Maven plugin bound to same phase will be executed in the same order as they are listed in the pom.xml

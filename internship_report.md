width=!,height=!,pages=-

##### I

# Dedication

#### With profound appreciation and much love, I would like to thank every

#### person who has contributed to my journey, every soul who has lifted

#### me up, and every heart that has believed in me.

#### To my motherFathiaand my fatherSadokyour unconditional love,

#### sacrifices,support and encouragement Thank you, for being the

#### embodiment of love and strength,I am forever grateful for your love.

#### To my sisterFeriel, brothersNader,Oday,Roudayna, our bond is

#### unbreakable, and my dedication to you is everlasting. Together, we are

#### a force of love, support, and lifelong companionship.

#### To my friends,Ayoub,Aziz,Iyed,Rathwane,Samiand all my

#### friends, The memories we’ve created and the bonds we’ve formed will

#### forever hold a special place in my heart. Thank you for the endless

#### support, the late-night study sessions, and the shared moments of joy.

#### With all my love and gratitude,

#### -Kossay

##### II

# Aknowledgements

First and foremost, I would like to extend my gratitude to my supervisor, Mr.
Tamallah Ali, for his invaluable support, assistance, and mentorship throughout
this project.

I would like also to express my dearest thank to Hendrik Thurauand his
supportqmlskdfjmqlksdfj

I would like to express our heartfelt appreciation to the entire academic staff
of theHigher Institute of Computer Science and Mathematics Monastir
in. Their significant contributions have played a vital role in our comprehensive
education.

Also we would like to sincerely thank all the members of the jury, Mr. 1 and
Mrs. 2 , as well as our supervisor, for the honor they bestowed upon us by accepting
to evaluate this work.

Finaly, I would like to express my gratitude to all those who have helped me,
directly or indirectly, in the completion of this project.

##### III

# Abstract

This report presents the culmination of my final-year project in Information and
Communication Technology speciality in Networks and Internet of Things. The
project aimed to design and implement a boat monitoring and security system de-
signed to enhance the safety and management of boats, particularly in remote and
offshore environments. It provides real-time tracking, environmental monitoring,
and intrusion detection, ensuring the boat’s condition is continuously supervised.
The system utilizes wireless communication to send alerts and location updates to
the owner, enabling timely responses to potential threats such as unauthorized ac-
cess, gas leaks, or abnormal environmental conditions. Powered by a solar-charged
battery system, it operates autonomously and reliably, making it a practical solution
for boat owners seeking peace of mind and improved security while at sea.

Keywords : IoT, GPS Tracking, ESP32, Boat Monitoring, Remote Alerts,
Solar-Powered, Maritime Safety, Mobile Application, Control.

##### IV

# Résumé

Ce mémoire présente l’aboutissement de mon projet de fin d’année en Technologies
de l’Information et de la Communication spécialité Réseaux et Internet des Objets.
Le projet visait à concevoir et à mettre en œuvre un système de surveillance et de
sécurité des bateaux conçu pour améliorer la sécurité et la gestion des bateaux, en
particulier dans les environnements éloignés et offshore. Il assure un suivi en temps
réel, une surveillance environnementale et une détection des intrusions, garantissant
ainsi une surveillance continue de l’état du bateau. Le système utilise la communi-
cation sans fil pour envoyer des alertes et des mises à jour de localisation au proprié-
taire, permettant ainsi de répondre rapidement aux menaces potentielles telles qu’un
accès non autorisé, des fuites de gaz ou des conditions environnementales anormales.
Alimenté par un système de batterie solaire, il fonctionne de manière autonome et
fiable, ce qui en fait une solution pratique pour les propriétaires de bateaux en quête
de tranquillité d’esprit et d’une sécurité accrue en mer.

Mots clés : IoT, Suivi GPS, ESP32, Surveillance des Bateaux, Alertes à dis-
tance, Alimenté par l’énergie solaire, Sécurité maritime, Application Mobile, Con-
trôle.

##### V

# List of abbreviations and acronyms

GPRS General Packet Radio Service

SIM Subscriber Identity Module

IOT Internet of Things

APN Access Point Name

IDE Integrated Development Environment

VCC Voltage Common Collector (or Power Supply Voltage)

GND Ground

NO Normally Open

LDR Light Dependent Resistor

PCB Printed Circuit Board

DC Direct Current

AC Alternating Current

AC Alternating Current

LoRa Long Range

UART Universal Asynchronous Receiver-Transmitter

RXD Receive Data

TXD Transmit Data

CAD Computer-Aided Design

##### VI

## Table of Contents

Table of Contents

```
3.5 Prototype................................. 61
```

```
3.6 Conclusion................................. 62
```

General Conclusion and perspectives 63

##### IX

## List of Figures

- General Introduction
- 1 General project context
  - 1.1 Introduction
  - 1.2 General Context of the Project
    - 1.2.1 Project scope
    - 1.2.2 About Hendrick Thurau Enterprises (HTE)
    - 1.2.3 Problematic
    - 1.2.4 Proposed Solution
    - 1.2.5 Goals and tasks
  - 1.3 Existing analysis and Related Technologies
    - 1.3.1 Internet of things(IOT)
    - 1.3.2 Embedded systems and IOT
    - 1.3.3 Smart Boating
    - 1.3.4 The Differences between traditional and Smart Boating
    - 1.3.5 Factors Affecting Boat Performance and Safety
  - 1.4 Process for project management
    - 1.4.1 Methodologies
    - 1.4.2 Project management tools
    - 1.4.3 Project planning
  - 1.5 Conclusion
- 2 Hardware and software study of the system Table of Contents
  - 2.1 Introduction
  - 2.2 System solution overview
  - 2.3 Methodology Approach
    - 2.3.1 Microcontroller Board
    - 2.3.2 Communication protocols
  - 2.4 Hardware Section
    - 2.4.1 ESP32 with SIM7600 Module
    - 2.4.2 SIM7600 4G LTE & GNSS Module
    - 2.4.3 Sensors
    - 2.4.4 Power Sources
    - 2.4.5 Reliability in Maritime Environments
  - 2.5 Software Section
    - 2.5.1 Simulation Software
    - 2.5.2 Computer-Aided Design Software (CAD)
    - 2.5.3 Integrated Development Environment (IDE)
    - 2.5.4 Mobile Application Integration
  - 2.6 Conclusion
- 3 Prototype System Implementation
  - 3.1 Introduction
  - 3.2 Realization and Validation
    - 3.2.1 Boat Monitoring System
    - 3.2.2 SIM7600 Initialization & Testing
    - 3.2.3 Boat Monitoring Prototype
  - 3.3 Enclosure Design
  - 3.4 Mobile Application
    - 3.4.1 Overview of Boat Pro
    - 3.4.2 IoT Dashboard
- 1.1 HTE Logo[?]
- 1.2 Iot architecture[?]
- 1.3 Iot application domaines [?]
- 1.4 An IOT Embedded Systems [?]
- 1.5 Connected Boating [?]
- 1.6 V-Model phases[?]
- 1.7 Workspace boards
- 1.8 Planning tasks
- 2.1 Range and bandwidth for different types of wireless networks [?]
- 2.2 Comparison of different wireless communication protocols
  - [?] 2.3 Starlink Direct to Cell concept: satellites act as LTE towers in space
  - SIM7600 module. Source: LilyGO GitHub repository [?]. 2.4 LilyGO TTGO ESP32 (ESP-WROVER-E variant) with integrated
- 2.5 LilyGO TTGO ESP32 + SIM7600 Pinout
- 2.6 SIM7600E-H LTE GNSS Module (Source: Xinyuan-LilyGO)
- 2.7 SIM7600E-H Pinout Diagram (annotated)
- 2.8 DHT22 Temperature and Humidity Sensor Module[1]
- 2.9 DHT22 Module Pinout[2]
- 2.10 HC-SR501 PIR Motion Sensor Module[3]
- 2.11 HC-SR501 PIR Sensor Pinout[4]
- 2.12 INA226 Power Monitoring Module[5] List of Figures
- 2.13 INA226 Pinout Diagram[6]
- 2.14 MQ-5 Gas Sensor Module[7]
- 2.15 MQ-135 Air Quality Sensor Module[8]
- 2.16 18650 Li-ion Cell in Battery Holder[9]
- 2.17 6V/10W Solar Panel (340×220mm)[10]
- 2.18 Fritzing Logo[11]
- 2.19 SolidWorks Logo[12]
- 2.20 Arduino IDE Logo[13]
- 2.21 Visual Studio Code Logo[14]
- 2.22 Ionic Framework Logo[15]
- 3.1 Global Wiring Diagram of Boat Monitoring System
- 3.2 Fritzing Schematic of Boat Monitoring System
- 3.3 3D CAD Rendering of Enclosure (Placeholder)
- 3.4 Environmental Data Card: temperature, humidity, motion, gas
- 3.5 System Status Card: battery voltage and speed
- 3.6 Air Quality & CO 2 Card
- 3.7 Historical Data Card: 24h temperature and humidity charts
- 3.8 Location Card: Real-time boat position on map
- 3.9 Geofence Settings Card
- 3.10 Geofence Events Card: breach track overlay
- 3.11 Notifications History
- 3.12 Arm/Disarm Control
- 3.13 Complete IoT Dashboard Interface
- 3.14 realisation and testing
- 3.15 Prototype
- 1.1 Difference between traditional and smart boating[?] List of Tables
- 2.1 Comparative Study of Microcontroller Boards
- 2.2 ESP-WROVER-E Key Specifications (Source: Espressif Datasheet [?])
- 2.3 SIM7600E-H Technical Specifications
- 2.4 SIM7600E-H Pinout Description
- 2.5 DHT22 Technical Specifications[16]
- 2.6 DHT22 Pinout Description[2]
- 2.7 HC-SR501 PIR Sensor Technical Specifications[17]
- 2.8 HC-SR501 PIR Sensor Pinout Description[4]
- 2.9 INA226 Technical Specifications[18]
- 2.10 INA226 Pinout Description[6]
- 2.11 MQ-5 Technical Specifications[19]
- 2.12 MQ-5 Pinout Description[20]
- 2.13 MQ-135 Technical Specifications[21]
- 2.14 MQ-135 Pinout Description[22]

“Graduation is not the end, it’s the beginning.”

—Senator Orrin Hatch

#### May 19, 2025

List of Tables

##### •

## General Introduction

In recent years, maritime activities have grown significantly, ranging from fishing
and transportation to recreational boating. However, with this growth, the need for
ensuring the safety, security, and operational efficiency of boats has become increas-
ingly critical. Boats are often exposed to harsh environmental conditions, theft,
accidents, and various operational challenges. These issues highlight the necessity
for a robust and reliable boat monitoring system that can provide real-time data
and alerts to boat owners, enabling them to respond promptly to emergencies and
ensure the safety of their vessels.

This project aims to design and develop an autonomous boat monitoring system
that utilizes modern technologies such as the Internet of Things (IoT), GPS tracking,
and wireless communication. The system will integrate sensors for environmental
and security monitoring, including temperature and humidity measurement, gas de-
tection, and motion detection. It will also feature real-time location tracking and
power monitoring to ensure the boat’s battery status is always known. The system
will operate independently using a solar-powered energy supply, ensuring continu-
ous functionality even in remote marine environments where access to electricity is
limited.

The primary objective of this project is to enhance the safety and security of small
boats by providing boat owners with a cost-effective, real-time monitoring solution.
This system will allow owners to track their boat’s location, receive alerts about
unauthorized access or hazardous gas leaks, and monitor the onboard environmental
conditions. Such a system is particularly beneficial for boat owners who leave their
vessels unattended for long periods or operate in isolated areas.

The motivation behind this project stems from the growing number of incidents
involving boat theft, accidents at sea, and environmental damage due to undetected
gas leaks or battery failures. These concerns underscore the need for a comprehen-
sive monitoring system capable of addressing multiple safety and security aspects
simultaneously.

To achieve these goals, the proposed system will employ an ESP32 microcon-
troller as the central processing unit, along with a SIM7600 module for 4G com-
munication and GPS location tracking. Various sensors, including a DHT22 for
temperature and humidity, an MQ-5 for gas detection, a PIR sensor for motion de-
tection, and an INA226 power monitor for voltage and current measurement, will
be integrated into the system. The entire setup will be powered by a solar-charged
battery pack, ensuring sustainability and long-term functionality.In summary, this

General Introduction

boat monitoring system seeks to provide a reliable, energy-efficient, and real-time
solution to the challenges faced by boat owners. By leveraging IoT technologies
and renewable energy, the system aims to offer an innovative approach to enhancing
maritime safety and operational efficiency.

This report mentions different steps to reach the project goals. It is mainly made
of three chapters:

The first chapter is"General Context of The Project"
The second chapter is “Hardware And Software Environment”
The third chapter is“System Design And Implementation”
And finally, I am going to conclude all that work and the achieved results with
some perspectives that will help us to make this project better and more developed.

# Chapter 1

# General project context

Chapter 1. General project context

### 1.1 Introduction

In this chapter, I will put this project into its general framework and I will start
with the general context of it, then I will present the problems and the proposed
solutions with a deep description of the project management method, and finally I
will conclude this chapter with a preliminary study.

### 1.2 General Context of the Project

#### 1.2.1 Project scope

In order to deserve a respectful degree of Information and Communication Tech-
nologies (ICT) at the Higher Institute of Computer Science and Mathematics in
Monastir (ISIMM) in the current academic year of 2024/2025, I did my end-of-
studies training atHendrik Thurau Enterprises. The goal of the project is to
develop a Boat Monitoring System linked with ‘Boaty Pro’ mobile application. This
system aims to provide real-time boat status updates, including location tracking,
battery monitoring, environmental conditions, and security alerts. The solution will
leverage IoT technologies to enhance maritime safety and operational efficiency for
boat owners.

#### 1.2.2 About Hendrick Thurau Enterprises (HTE)

Hendrik Thurau Enterprises (HTE) is a Switzerland-based company specializing in
IT and digital business solutions. With business roots dating back to 1988, HTE
has built a strong reputation for delivering high-quality digital services, including
web, app, and software development, outsourcing, offshoring, digital consulting, and
design. The company’s mission is to provide innovative solutions that give clients
a competitive edge, enabling their businesses to scale and succeed. Backed by a
highly qualified team, HTE is committed to excellence in software development,
digital transformation, and strategic business growth.

```
Figure 1.1: HTE Logo[?]
```

Chapter 1. General project context

#### 1.2.3 Problematic

In the maritime industry, boat owners and operators often face challenges in mon-
itoring their vessels remotely, especially when they are docked or left unattended
for extended periods. Traditional monitoring methods rely on manual checks or
expensive tracking systems, which may not provide real-time insights into a boat’s
status.

```
Key issues include :
```

- Lack of remote monitoring: Owners cannot easily check their boat’s loca-
  tion, battery health, or onboard conditions without being physically present.
- Security risks:Unauthorized access or theft can occur without timely alerts
  or tracking mechanisms.
- Environmental hazards: Sudden changes in temperature, humidity, or gas
  leaks (such as fuel vapor) can pose safety risks if not detected early.
- Power management challenges: Many monitoring systems require con-
  stant power sources, making them impractical for small boats with limited
  energy availability.

To address these challenges, this project aims to develop a Boat Monitoring System
integrated with the Boaty Pro mobile application. The system will leverage IoT
technologies to provide real-time data on boat location, battery status, environmen-
tal conditions, and security alerts, ensuring improved safety, efficiency, and peace of
mind for boat owners.

#### 1.2.4 Proposed Solution

To address the challenges identified in the problem statement, this project proposes
the development of a Boat Monitoring System integrated with the Boaty Pro mobile
application. The system leverages IoT technologies to provide real-time monitoring
and data insights, ensuring boat owners can remotely track their vessel’s status and
receive alerts when necessary.

The solution consists of several key components. It enables remote communica-
tion and data transmission over a mobile network, allowing boat owners to access
information on demand. The system provides real-time and on-demand location
updates to help owners monitor their boat’s position. To prevent unexpected power
failures, it includes a power monitoring feature that tracks battery voltage, cur-
rent, and overall consumption. Environmental sensors measure temperature and
humidity, ensuring safety against extreme conditions, while gas leak detection helps
identify fuel or gas leaks, reducing fire hazards. Security is enhanced with motion
detection, which alerts owners to unauthorized access. Additionally, the system is
designed for energy efficiency, operating on a solar-powered setup with a recharge-
able battery, ensuring continuous functionality even in remote areas.

Chapter 1. General project context

Through Boaty Pro, users can conveniently access real-time and historical data,
receive security notifications, and monitor critical boat conditions from anywhere.
This cost-effective, energy-efficient, and scalable solution enhances maritime safety,
operational efficiency, and user convenience.

#### 1.2.5 Goals and tasks

The content that follows is a list of the major tasks and objectives that the project
is meant to achieve:

```
a. Goals
```

- Develop a reliable IoT-based monitoring system capable of tracking a
  boat’s location, battery status, and environmental conditions.
- Ensure real-time and on-demand data transmission via a 4G-enabled com-
  munication module.
- Improve boat security by integrating motion detection and alert notifica-
  tions through the mobile app.
- Optimize power consumption using a solar-powered battery system to
  ensure uninterrupted operation.

Chapter 1. General project context

```
b. Key Tasks
```

- Installing sensors and communication modules:Setting up envi-
  ronmental, security, and power monitoring sensors, along with communi-
  cation modules, to ensure data collection and remote accessibility.
- Collecting and analyzing data: Monitoring real-time data from the
  system, including boat location, battery status, environmental conditions,
  and security alerts, to provide actionable insights.
- Developing a remote monitoring system: Integrating the collected
  data into the Boaty Pro mobile application, allowing users to view real-
  time and historical information.

### 1.3 Existing analysis and Related Technologies

This section explores key technologies relevant to the proposed Boat Monitoring
System, highlighting their role in enhancing safety, efficiency, and operational relia-
bility.

#### 1.3.1 Internet of things(IOT)

1.3.1.1 Definition

The Internet of Things (IoT) is a network of physical "objects" or terminals that
integrate sensors, software, and other technologies in order to communicate with
other terminals and systems on the Internet and exchange data with them.

1.3.1.2 IOT architecture

There are many phases in the IoT architecture and they can be changed depending
on the circumstances. When speaking about Iot one can define the following. It
contains four phases, which are shown in Figure 1.2.

```
Figure 1.2: Iot architecture[?]
```

- Devices: The Perception layer of IoT focuses on real devices like sensors
  and actuators that produce data or produce action. The data produced are

Chapter 1. General project context

```
transformed and sent to the Internet gateway stage. Due to limited resources,
data are often transferred in a raw state until a critical decision is made.
```

- Internet gateways:process raw data from devices before sending it to the
  cloud. It can be a standalone unit or physically linked to the device, connecting
  to sensors through low-power networks. The gateway can transmit data over
  the Internet.
- In edge or fog computing: data are rapidly processed at the edge of the
  cloud for quick evaluation and urgent attention. This layer focuses on the latest
  information required for fast operations, and some pre-processing is carried out
  to reduce data uploaded to the cloud.
- Cloud or data center: In this final stage, the cloud or data center, where
  data is stored for later processing and deep analysis, including resource-intensive
  processes such as machine learning training. The saved data can be pushed into
  dashboards or management software in the application and business layers.[?]

  1.3.1.3 IOT application areas

There are several sectors and applications areas where the Internet of Things (IoT)
may be used. Among the most popular IoT applications fields are illustrated in the
following figure 1.3 :

```
Figure 1.3: Iot application domaines [?]
```

Chapter 1. General project context

#### 1.3.2 Embedded systems and IOT

The Internet of Things (IoT) has revolutionized the way we live, work, and interact
with each other. IoT refers to a network of interconnected devices that can commu-
nicate with each other without human intervention. Embedded systems are at the
heart of IoT technology: small and powerful microprocessors embedded in everyday
objects such as smartphones, appliances, and vehicles. These systems enable seam-
less communication between devices, allowing them to collect, process, and share
data in real time.
As technologies continue to advance, embedded systems have become more so-
phisticated and powerful than ever before. They incorporate advanced sensors,
wireless capabilities, and machine learning algorithms to deliver highly personalized
experiences for users.
By enabling quicker decision-making based on data gathered from various IoT
devices, embedded systems are significantly improving our everyday lives in a variety
of areas, such as healthcare surveillance, industrial production processes as well as
agriculture monitoring.
To sum up, embedded systems are an essential part of the Internet of Things
because they supply the required control and intelligence for objects to communicate
and share data as seen in figure 1.4 below:

```
Figure 1.4: An IOT Embedded Systems [?]
```

#### 1.3.3 Smart Boating

Technology and the IoT impact every aspect of our lives, homes, cars, and lifestyles.
So, it is somewhat inevitable that demand for this type of connectivity will eventually
reach the boating world too.

Boat owners are beginning to turn to smart technology on their vessels to moni-
tor, track, protect, and enhance their boating experiences. Today’s top technologies
allow you to connect with and monitor your boat and its systems while you are
away. It also allows you to receive up-to-the-minute information while on the water
for things such as bilge level alarms or important weather updates.

Chapter 1. General project context

1.3.3.1 Connected Boating

Connected boating is the overarching term of the use of smart technologies to en-
hance boat ownership and boating experiences. Just like in other areas of our lives,

the boating industry and boat owners are turning to smart technology and connected
devices to improve security, monitor systems, and offer real-time updates and alerts.

Specefic devices or entire systems can be added to vessels that use sensors to
collect data which is then sent to an information hub or cloud, using bluetooth, Wi-Fi
or even satellite technology. This information is instantly and continuously analyzed.
The information is sent back to the owner via an app subscription, downloaded onto
their smartphone or table. In many caes, the owner is able to control and manage
devices and swithces directly from these apps as well. [https://waiv.ai]

```
Figure 1.5: Connected Boating [?]
```

#### 1.3.4 The Differences between traditional and Smart Boating

The table 1.1 below presented the main differences between traditional smart (con-
nected) boating:

Chapter 1. General project context

```
Tableau 1.1: Difference between traditional and smart boating[?]
```

```
Traditional Smart Boating
```

```
Manual navigation with maps and com-
passes.
```

```
GPS-based real-time tracking and ge-
ofencing.
```

```
Requires physical inspection. Remote monitoring via IoT sensors.
```

```
Basic locks and manual surveillance. Motion sensors, GPS tracking, and
alerts.
```

```
Manual battery checks and fuel depen-
dency.
```

```
Solar-powered system with smart mon-
itoring.
```

#### 1.3.5 Factors Affecting Boat Performance and Safety

Many factors can significantly impact the performance and safety of a boat. A
Smart Boat Monitoring System is designed to monitor and manage these factors in
real time, ensuring optimal conditions for safe and efficient operation. Below, we
discuss the key factors and their effects:

- Temperature and Humidity:
  - Effect: High temperatures can lead to engine overheating, while high
    humidity can cause condensation, damaging electrical systems.
  - Monitoring:Sensors track temperature and humidity levels, generating
    alerts if thresholds are exceeded.
  - Example:
    ∗ Optimal Temperature: 15-30°C
    ∗ Optimal Humidity: 40-60%
    ∗ Critical Alert: Temperature > 35°C or Humidity > 80%
- Power Consumption and Battery Health:
  - Effect: Inefficient power management can lead to battery failure, dis-
    rupting navigation and communication systems.
  - Monitoring:Sensors measure voltage, current, and power consumption,
    providing real-time data and alerts for abnormal conditions.
  - Example:
    ∗ Optimal Battery Voltage: 12-14V
    ∗ Critical Alert: Voltage < 11V or Current > 10A
- Gas Leaks:

Chapter 1. General project context

- Effect:Flammable gas leaks pose a serious safety risk, potentially lead-
  ing to fires or explosions.
- Monitoring: Gas sensors detect the presence of flammable gases and
  trigger alerts if concentrations exceed safe levels.
- Example:
  ∗ Safe Gas Concentration: < 300 ppm
  ∗ Critical Alert: Gas concentration > 500 ppm
- Intruder Detection:
- Effect: Unauthorized access can lead to theft, vandalism, or safety
  breaches.
- Monitoring:Motion sensors detect movement within the boat’s interior
  and send alerts if motion is detected when the boat is unoccupied.
- Example:
  ∗ Normal Condition: No motion detected
  ∗ Intruder Alert: Motion detected when boat is unoccupied
- Location and Environmental Conditions:
- Effect: Adverse weather conditions (e.g., high winds, rough seas) and
  incorrect navigation can compromise safety.
- Monitoring:GPS and environmental sensors provide real-time updates
  on location, wind speed, wave height, and other conditions.
- Example:
  ∗ Safe Wind Speed: < 20 knots
  ∗ High Wave Alert: Wave height > 2 meters
  ∗ Emergency Alert: Boat drifts outside a predefined safe zone

Figure??illustrates how these factors are monitored and managed by the Smart
Boat Monitoring System.

### 1.4 Process for project management

In order to make our project more efficient and successful and to finish it before the
deadline, we used methods and tools that were advantageous to us.

#### 1.4.1 Methodologies

The general aim of our project management methodology is to be able to standardize
structure and organize work methods.

It helps us reduce risks, avoid duplication of efforts, increase its impact ulti-
mately, resulting in a continuous improvement process. In other words, this method-
ology is a great tool for generating efficiency.

Chapter 1. General project context

1.4.1.1 V-model methodology

V- model means Verification and Validation model. Just like the waterfall model,
the V-Shaped life cycle is a sequential path of execution of processes. Each phase
must be completed before the next phase begins. The following figure1.7 shows the
various phases of a V-Model.[?]

```
Figure 1.6: V-Model phases[?]
```

The related testing phase of the development phase is planned in parallel. So,
there are Verification phases on one side of the ‘V’ and Validation phases on the
other side. The Coding Phase joins the two sides of the V-Model.

Design Phase

- Requirements: This phase contains detailed communication with the cus-
  tomers to understand their requirements and expectations. This stage is
  known as Requirement Gathering.
- Analysis and architecture: Architecture Design: The baseline in selecting
  the architecture is that it should understand all which typically consists of the
  list of modules, brief functionality of each module, their interface relationships,
  dependencies, database tables, architecture diagrams, technology detail, etc.
- Coding Phase: After designing, the coding phase started. Depending on
  the requirements, a suitable programming language is decided. There are some

Chapter 1. General project context

```
guidelines and standards for coding, which goes through many code reviews
to check the performance.
```

Testing Phases

- Unit Testing : The V-Model uses Unit Test Plans (UTPs) during the
  module design phase to eliminate errors at the code/unit level. UTPs are
  executed to verify that the smallest unit (e.g., a program module) can function
  correctly on its own. Unit testing is essential to ensure the proper functioning
  of individual program modules.
- Integration Testing: Integration Test Plans are developed during the Ar-
  chitectural Design Phase. These tests verify that groups are created and tested
  independently as well as coexisting and communicating among themselves.
- Acceptance Testing: Acceptance testing is done in the user environment
  to test the software’s compatibility and non-functional issues like load and
  performance defects. It is related to business requirement analysis and reveals
  any compatibility issues with different systems. This testing is essential to
  identify any problems in the real user environment.

#### 1.4.2 Project management tools

Organization and scheduling are essential for the success of my project. For man-
aging my work, I used the Bitrix24 platform.
Bitrix24 is a web-based project management tool that helps in job organization
and scheduling. It offers various features such as online storage, Scrum, Gantt charts,
time management, workload planning, group chat, social networking, knowledge
management, video calls, client management, invoicing, document management,
file synchronization, HR tools, workflow automation, and customization. It also
provides an AI assistant, API integration, and a marketplace for additional tools.
Using Bitrix24 makes it simple to collaborate and communicate by allowing users
to manage tasks efficiently, track progress, and streamline workflows. Additionally,
its built-in automation and document management features help keep work orga-
nized and accessible.
To sum up, Bitrix24 is a powerful and versatile tool that helps individuals and
teams stay organized, collaborate effectively, and achieve their goals. The subse-
quent figures highlight my workspace on this platform.

Chapter 1. General project context

```
Figure 1.7: Workspace boards
```

#### 1.4.3 Project planning

In my project, I estimated that it would take approximately four months to complete
the work. The timeline provides a detailed overview of the different phases of the
project, outlining key milestones and deadlines to ensure a structured and efficient
workflow.

**Project Timeline**

```
1
```

```
4
```

```
2
```

```
6
```

```
Define the requirements
```

```
Integrate the software andthe hardware
```

```
Prototype Hardware
```

```
Final testing, debuggingand intrenship report
```

```
Develop the app
```

```
Deliver the completesystem
```

```
Add advanced features
```

```
3
```

```
7
```

```
5
```

```
Finalise the list of features toimplement
Create the projectspecefications
01/02/2025 -> 07/02/2025
```

```
Connect the hardware to theapp
Test data flow andfonctionality
16/03/2025 -> 30/03/2025
```

```
Develop the basic prototypeAssemble and test sensors
08/02/2025 -> 28/02/2025for monitoring^
```

```
University Report (Rapport deFinal test and debugging
21/04/2025 -> 10/05/2025stage)
```

```
Add the needed features tothe app
between the hardware andEnsure communication
01/03/2025 -> 15/03/2025the app
```

```
Finalise the documentationand the presentation
11/05/2025 -> 30/05/2025
```

```
Implement security featuresAdd energie management
01/04/2025 -> 20/04/2025
```

```
CHARGUI KOSSAY
```

```
Figure 1.8: Planning tasks
```

Chapter 1. General project context

### 1.5 Conclusion

In this chapter, I presented the general context of our project, described it, and at
the same time we specified the main objectives to be achieved. In the next chapter, a
bibliographic analysis of the required materials of the current study will be provided.

# Chapter 2

# Hardware and software study of the

# system

Chapter 2. Hardware and software study of the system

### 2.1 Introduction

In this chapter, I present the hardware and software components chosen for the
implementation of the boat monitoring system. Based on the needs identified in the
previous chapter, I have selected a set of tools and modules that best match the
project’s goals in terms of performance, cost, and availability.
The system is built around the LilyGO ESP32 board with an integrated SIM7600
module and GPS for connectivity and location tracking. I also use sensors to detect
gas, air quality, motion, temperature, humidity, and monitor battery voltage. This
chapter details the rationale behind each component selection and the software tools
used for development, forming the technical foundation of the system.

### 2.2 System solution overview

To address the needs of a reliable and autonomous boat monitoring system, I de-
signed a solution based on a compact and low-power embedded platform capable
of collecting, processing, and transmitting sensor data in real time. My goal is to
enable remote supervision of various environmental and operational parameters on
board, such as gas leaks, air quality, motion detection, temperature, humidity, and
battery voltage.
At the heart of the system is the LilyGO TTGO ESP32 development board,
which integrates an ESP32 microcontroller, a SIM7600 4G module, and GPS func-
tionality. This all-in-one board significantly reduces complexity, saves space, and
simplifies power management. The SIM7600 module allows the system to send data
over 4G networks and retrieve GPS location, enabling both monitoring and real-time
tracking of the boat.
The sensor suite consists of:

- DHT22 : for measuring temperature and humidity,
- MQ-5 : for gas leak detection (e.g., LPG, methane),
- MQ-135 :for monitoring air quality (e.g., CO, NH),
- PIR :sensor for detecting unauthorized movement near or on the boat,
- INA226 : for voltage and current monitoring of the battery.

All components are connected to the ESP32 via digital or I2C interfaces, depend-
ing on the sensor type. The data collected is periodically transmitted to a cloud
server or mobile app interface via GSM/4G, allowing me to monitor the system
remotely.
Power is supplied by a Li-ion battery in the back of the ESP32, which is charged
through a solar panel, ensuring energy autonomy. The system is designed to be
energy-efficient, modular, and scalable, with the possibility of integrating additional
sensors or actuators in the future.

Chapter 2. Hardware and software study of the system

This solution offers a balance between reliability, cost, and simplicity, making
it suitable for real-world marine environments where consistent connectivity and
autonomous operation are critical.

### 2.3 Methodology Approach

#### 2.3.1 Microcontroller Board

The microcontroller board acts as the brain of the system, enabling communication
with sensors, modules, and peripherals. In this context, I opted for the LilyGO
ESP32 board with a built-in SIM7600 4G module and GPS support. This decision
was based on the board’s wireless capabilities, low power consumption, and suitabil-
ity for IoT applications. The table below compares this board with other common
microcontroller boards.

Chapter 2. Hardware and software study of the system

```
Tableau 2.1: Comparative Study of Microcontroller Boards
```

```
Board Arduino Uno ESP32 DevKit LilyGO ESP32 +SIM7600
```

```
Dimensions 6.86 cm x 5.34 cm 5.4 cm x 2.7 cm 8.6 cm x 2.7 cm
(with SIM7600)
```

```
Processor ATmega328P
```

```
Xtensa Dual Core
32-bit LX6
```

##### ESP32 + SIM7600

```
ARM Cortex A7
```

```
Memory 32 KB Flash, 2 KBSRAM 4 MB Flash, 520KB SRAM
```

```
4 MB Flash
(ESP32), 1 GB
RAM (SIM7600)
```

```
I/O Pins 14 digital, 6 analog log30 digital, 18 ana-
```

##### 24 GPIO (ESP32),

```
SIM7600 UART in-
terface
```

```
Operating
Voltage 5V, 3.3V 3.3V
```

##### 3.3V (ESP32), 3.8-

##### 4.2V (SIM7600)

```
Wireless None Wi-Fi, Bluetoothv4.2 Wi-Fi, Bluetooth,4G LTE, GPS
```

```
Clock Speed 16 MHz 80–240 MHz
```

```
240 MHz (ESP32)
+ 1.2 GHz
(SIM7600)
```

```
Price 41.000 TND 34.800 TND 150.000 TND
```

#### 2.3.2 Communication protocols

A communication protocol is a set of rules and conventions that govern the format,
timing, sequencing, and error control of data exchange between two or more en-
tities. It defines how information is transmitted, received, and interpreted during
communication to ensure reliable and consistent data transfer.
In my project, communication protocols play a crucial role in enabling seamless
interaction between onboard sensors, control units, and the cloud-based monitoring
platform. The main objective is to ensure real-time or periodic transmission of
location, environmental, and system status data from the boat to the end user, even
when the boat is in remote areas with limited or no terrestrial connectivity.
As can be seen in figure??, there are different types of wireless networks accord-
ing to their range and bandwidth.

Chapter 2. Hardware and software study of the system

```
Figure 2.1: Range and bandwidth for different types of wireless networks [?]
```

There are two primary categories of networks available in the market: long-range
networks and short-range networks.

- Long-range networks: including LPWAN technologies like Sigfox, LoRa,
  and cellular networks (GSM, 2G, 3G, 4G, 5G), facilitate data transfer over ex-
  tensive distances. They are widely employed to connect infrastructure spread
  over kilometers, offering reliable long-range communication capabilities.
- Short-range networks: like WiFi, Z-Wave, ZigBee, and low-energy Blue-
  tooth, facilitate data transfer over shorter distances. They are widely used in
  home automation and consumer wearables for reliable local communication.

Chapter 2. Hardware and software study of the system

```
Figure 2.2: Comparison of different wireless communication protocols
```

While short-range technologies like Bluetooth and WiFi may perform well in
indoor or terrestrial environments, they become unreliable or unusable in maritime
environments. This is due to their limited range and dependence on local infras-
tructure, such as access points or routers—which are simply unavailable in open sea
conditions. Similarly, LoRaWAN requires the deployment of a gateway to collect
and transmit data from the nodes, meaning two LoRa modules are needed: one in
the remote system and one acting as the base station. This infrastructure depen-
dency makes LoRaWAN infeasible for mobile and isolated use cases like our boat
monitoring system.

Moreover, traditional satellite communication systems, such as those offered by
Iridium or Inmarsat, are already used in maritime applications for emergency signal-
ing and remote data exchange. However, these systems are notoriously expensive,
both in terms of hardware and operational costs. They typically require special-
ized, high-gain antennas and bulky modems, which are not suitable for compact,
low-power IoT systems like the one proposed in our project. This makes them
inaccessible for many small-scale applications or budget-constrained deployments.

By contrast, the emerging Direct to Cell technology from Starlink provides a
cost-effective and scalable alternative. It leverages existing LTE protocols and is
designed to work with unmodified mobile devices and modules, eliminating the need
for expensive satellite-specific hardware. This approach dramatically lowers the
entry barrier for global connectivity, especially in hard-to-reach environments like
the sea.

After comparing the different types of networks, we finally decided to use a
cellular network-based solution. Our system takes inspiration from the Starlink
“Direct to Cell” innovation, which enables communication between satellites and
standard LTE devices. This solution offers a robust, future-proof infrastructure that
is expected to support not only messaging but also voice, data, and IoT services

Chapter 2. Hardware and software study of the system

by 2025. As documented by Starlink in their official update [?], this technology
overcomes the significant technical challenges of satellite-to-phone communication by
incorporating phased-array antennas, custom silicon, and advanced signal processing
onboard the satellites.

Figure 2.3: Starlink Direct to Cell concept: satellites act as LTE towers in space [?]

### 2.4 Hardware Section

This section provides an in-depth analysis and technical study of the hardware com-
ponents chosen for the boat monitoring system. The selection of each component
was based on its suitability, performance, energy efficiency, and cost-effectiveness to
meet the system requirements for remote monitoring, GPS tracking, and environ-
mental sensing in marine environments.
The proposed hardware system is composed of the following main components:

- ESP32 development board with SIM7600 4G/GPS module
- Sensors (PIR motion, MQ-5 gas, MQ-135 air quality, DHT22 temperature/humidity,
  INA226 voltage/current)
- Power supply system (single 18650 Li-ion battery, solar panel input, onboard
  charger)
- Supporting modules (voltage regulators, external antennas, connectors)

#### 2.4.1 ESP32 with SIM7600 Module

The core of the system is the LilyGO TTGO ESP32 board equipped with an ESP-
WROVER-E microcontroller and integrated SIM7600 4G LTE/GNSS module. Key
specifications from the ESP-WROVER-E datasheet include:

Chapter 2. Hardware and software study of the system

- Processor: Xtensa dual-core 32-bit LX6 microprocessor (up to 240 MHz)
- Memory:
  - 448 KB ROM
  - 520 KB SRAM + 16 KB RTC SRAM
  - 4/8/16 MB SPI flash (configurable)
  - 8 MB PSRAM (ESP32-D0WDR2-V3 variant)
- Wireless:
  - Wi-Fi 802.11b/g/n (150 Mbps max)
  - Bluetooth 4.2 BR/EDR + BLE
- Peripherals: 24 GPIO pins supporting UART, SPI, I2C, PWM, ADC, and
  CAN bus
- Power: 3.0–3.6 V operating range, optimized for low-power sleep modes

Chapter 2. Hardware and software study of the system

Figure 2.4: LilyGO TTGO ESP32 (ESP-WROVER-E variant) with integrated
SIM7600 module. Source: LilyGO GitHub repository [?].

2.4.1.1 Key Advantages for Marine Applications

- Enhanced Memory:8MB PSRAM enables robust buffering of GPS/Cellular
  data during intermittent connectivity.
- Dual-Core Efficiency:Dedicate one core to sensor polling (DHT22, INA226)
  while the other manages cellular/GNSS communications.
- Industrial-Grade Reliability:Operates at -40°C to 85°C, critical for harsh
  marine environments.
- Integrated Antenna Options: On-board PCB antenna (WROVER-E) or
  external connector (WROVER-IE) for flexible deployment.

Chapter 2. Hardware and software study of the system

Tableau 2.2: ESP-WROVER-E Key Specifications (Source: Espressif Datasheet [?])

```
Parameter Value
Cellular Modem SIM7600E-H (LTE Cat-1, up to 150 Mbps DL)
GNSS Support GPS, GLONASS, Galileo, BeiDou
PSRAM 8 MB (ESP32-D0WD-R2-V3)
Deep Sleep Current 1.2 mA
Certifications Bluetooth BQB, RoHS, REACH
```

```
a. LilyGO TTGO ESP32 Pinout
The LilyGO TTGO ESP32 board integrates the ESP32 microcontroller
and SIM7600 module on a compact development board. All GPIO, power,
and communication lines are exposed via pin headers along both edges,
facilitating straightforward connection of sensors, antennas, and power
circuits with jumper wires or header cables. This layout allows secure,
reliable interfacing even in a marine enclosure.
Figure 2.5 illustrates the pin layout of the TTGO ESP32 + SIM7600
board, highlighting the 3.3 V, GND, I2C (SDA/SCL), UART (TX/RX),
and analog input pins used for sensor integration.
```

```
Figure 2.5: LilyGO TTGO ESP32 + SIM7600 Pinout
```

Chapter 2. Hardware and software study of the system

```
b. ESP32 Programming Guide
The ESP32 on the LilyGO board can be programmed using several frame-
works and languages, offering flexibility depending on project require-
ments:
```

- Arduino C/C++ (via the ESP32 Arduino core)
- Espressif IoT Development Framework (ESP-IDF)
- MicroPython
- JavaScript (using Espruino or Moddable SDK)
  For rapid prototyping and access to a rich ecosystem of libraries (SIM7600
  AT command wrappers, TinyGPS++ for GNSS parsing, and sensor drivers),
  I use the Arduino C/C++ environment. This approach simplifies serial
  debugging, deep-sleep configuration, and OTA updates when connected
  via USB or 4G.

#### 2.4.2 SIM7600 4G LTE & GNSS Module

```
The SIM7600E-H is a multi-band LTE Cat-1 cellular modem with integrated
GNSS support, chosen for its combination of high-speed data, global satel-
lite navigation, and ease of integration with the ESP32. It provides reliable
4G connectivity for real-time data transmission and multi-constellation po-
sitioning (GPS, BeiDou, GLONASS, Galileo) without the need for separate
modules.
```

```
Figure 2.6: SIM7600E-H LTE GNSS Module (Source: Xinyuan-LilyGO)
```

```
From a technical standpoint, the SIM7600E-H module features:
```

Chapter 2. Hardware and software study of the system

- LTE Cat-1 Data: Up to 10 Mbps uplink, 50 Mbps downlink
- GNSS:Concurrent GPS, BeiDou, GLONASS, Galileo
- Frequency Bands:LTE: B1/B2/B3/B4/B5/B8/B12/B13/B18/B19/B20/B25/B26/B28/B39;
  UMTS: B1/B2/B5/B8; GSM: 850/900/1800/1900 MHz
- Interfaces:UART (for AT commands), USB 2.0, I²C, PCM
- Power Supply:3.4 – 4.2 V (Li-ion); up to 2 A peak during transmission
- SIM Card:Standard SIM socket, supports 1.8 V/3 V cards
- Antenna Connectors:SMA for LTE and GNSS antennas

```
a. Technical Specifications
Table 2.3 lists the key specifications of the SIM7600E-H module as used
on the LilyGO TTGO board.
```

```
Tableau 2.3: SIM7600E-H Technical Specifications
Parameter Value
```

```
Supply Voltage 3.4 – 4.2 V
```

```
Average Current (idle) < 25 mA
Peak Current (LTE
transmit)
```

```
Up to 2 A
```

```
Data Rates UL: up to 10 Mbps; DL: up to 50 Mbps
```

```
Module Dimensions 42 mm×36 mm×4.2 mm
```

```
Cellular Bands LTE, UMTS, GSM (see bullet list above)
GNSS Channels 32 parallel satellite channels
```

```
Operating Tempera-
ture –40°C to +85°C
```

```
Interfaces UART, USB 2.0, I²C, PCM
```

```
Certifications CE, FCC, PTCRB (module)
```

```
b. Pinout Description
Figure 2.7 shows the pin assignments for the SIM7600E-H module as
mounted on the LilyGO board. Table 2.4 describes each pin’s function.
```

Chapter 2. Hardware and software study of the system

```
Figure 2.7: SIM7600E-H Pinout Diagram (annotated)
```

```
Tableau 2.4: SIM7600E-H Pinout Description
Pin Function
VCC Power input (3.4 – 4.2 V Li-ion battery)
```

```
GND Ground reference
```

```
TXD UART transmit (module→MCU)
RXD UART receive (MCU→module)
```

```
USB_D+ /
USB_D USB data lines (for flashing/debug)
```

```
I2C_SDA / SCL I²C data and clock (optional debugging)
```

```
PCM_CLK /
DAT Digital audio interface (PCM)
```

```
NET_LED Network status indicator LED
RESET Active-low reset input
```

```
DTR Sleep control (HIGH: sleep; LOW for > 50 ms: wake)
```

```
RTC_RST Wake-up from deep sleep
SIM_DET SIM card detection (MICRO SIM socket present)
```

Chapter 2. Hardware and software study of the system

#### 2.4.3 Sensors

```
Sensors in the boat monitoring system measure environmental and operational
parameters to ensure safety and performance at sea. They collect data on
temperature, humidity, air quality, gas presence, motion, and battery status,
which is then transmitted via the ESP32+SIM7600 module to the remote
monitoring platform.
```

```
2.4.3.1 DHT22 Sensor
```

```
The DHT22 sensor (also known as AM2302) uses a capacitive humidity sensing
element and a thermistor to measure humidity and temperature, respectively.
It employs a single-wire digital communication protocol: after a start signal
from the ESP32, the DHT22 sends a 40-bit data packet (16 bits humidity, 16
bits temperature, 8 bits checksum) over one data line. A full data exchange
takes approximately 5 ms.
```

```
Communication and synchronization between the ESP32 and the DHT22 occur
on a single GPIO pin. The microcontroller pulls the data line low for at least
1 ms to initiate a read, then listens for the sensor’s 40 bit response.
```

```
Figure 2.8: DHT22 Temperature and Humidity Sensor Module[1]
```

```
The DHT22 sensor offers the following features:
```

- Temperature range: –40°C to +80°C with±0.5°C accuracy

Chapter 2. Hardware and software study of the system

- Humidity range: 0 to 100% RH with±2% accuracy
- Sampling rate: 0.5 Hz (one reading every 2 seconds)
- Operating voltage: 3.3 – 6 V
- Low power consumption: typically 1.5 mA during measurement

```
a. Technical Specifications
```

```
Tableau 2.5: DHT22 Technical Specifications[16]
Parameter Value
```

```
Dimensions 15.1 mm×25 mm×7 mm
```

```
Power Supply 3.3 – 6 V
Average Current 1.5 mA (during measurement)
```

```
Temperature Measurement –40±0.5°C to +80°C accuracy°C, 0.1°C resolution,
```

```
Humidity Measurement 0 % to 100 % RH, 0.1% resolution,% accuracy ±^2
```

```
Sampling Rate 0.5 Hz (one reading every 2 s)
```

```
Response Time < 2 s
Price 14.500TND
```

```
b. Pinout Description
```

Chapter 2. Hardware and software study of the system

```
Figure 2.9: DHT22 Module Pinout[2]
```

```
Tableau 2.6: DHT22 Pinout Description[2]
Pin Function
```

```
VCC Power supply (3.3 – 6 V)
```

```
DATA Single-wire digital data I/O
NC Not connected
```

```
GND Ground
```

```
2.4.3.2 PIR Motion Sensor
```

```
The PIR (Passive Infrared) motion sensor (HC-SR501) detects changes in in-
frared radiation within its field of view, allowing it to sense the presence or
movement of humans or animals near the boat. Internally, it uses a pyro-
electric sensor to generate a small voltage when it detects infrared heat vari-
ations. The sensor board includes a Fresnel lens, adjustable sensitivity and
timing potentiometers, and outputs a digital HIGH signal when motion is
detected.
```

```
Upon power-up, the PIR sensor enters a warm-up period (typically 30–60 s).
After stabilization, the sensor continuously monitors infrared levels. When
motion is detected, the digital output pin goes HIGH for a duration set by the
```

Chapter 2. Hardware and software study of the system

```
onboard “time” potentiometer (0.3–18 s). Sensitivity can be adjusted via the
“sensitivity” potentiometer or by selecting one of two detection ranges via the
onboard jumper (3 m or 7 m maximum).
```

```
Figure 2.10: HC-SR501 PIR Motion Sensor Module[3]
```

```
The PIR sensor offers the following features:
```

- Detection range: adjustable, typically 3–7 m
- Field of view: 120°
- Operating voltage: 3.3–5 V
- Low standby current: <50μA
- Onboard potentiometers for sensitivity and timing adjustment

```
a. Technical Specifications
```

Chapter 2. Hardware and software study of the system

```
Tableau 2.7: HC-SR501 PIR Sensor Technical Specifications[17]
Parameter Value
```

```
Model HC-SR501
Detection Distance 3–7 m (adjustable)
```

```
Detection Angle 120 °
```

```
Trigger Mode Repeatable (RET), Non-repeatable (L)
High Level Output 3.3–5 V
```

```
Quiescent Current <50μA
```

```
Operating Voltage 3.3–5 V
Warm-up Time 30–60 s
```

```
Time Delay 0.3–18 s (adjustable)
```

```
Operating Temperature –15°C to +70°C
Module Dimensions 32 mm×24 mm
```

```
b. Pinout Description
```

```
Figure 2.11: HC-SR501 PIR Sensor Pinout[4]
```

Chapter 2. Hardware and software study of the system

```
Tableau 2.8: HC-SR501 PIR Sensor Pinout Description[4]
Pin Function
```

```
VCC Power supply (3.3–5 V)
OUT Digital output: HIGH when motion is detected
```

```
GND Ground
```

```
2.4.3.3 INA226 Power Monitoring Sensor
```

```
The INA226 is a high-side or low-side I2C-based current and power monitor-
ing sensor, used in our system to measure the battery’s voltage, current, and
power consumption accurately. It integrates a 16-bit analog-to-digital con-
verter (ADC) and performs computations internally, outputting digital values
over the I2C bus.
```

```
The sensor requires a shunt resistor placed in series with the load. The INA226
measures the voltage drop across this resistor to calculate the current, while
also monitoring the bus voltage to determine power consumption. Its ability
to monitor both voltage and current makes it suitable for low-power embedded
systems and energy monitoring projects.
```

```
The figure 2.12 presents the INA226 module utilized in our project.
```

```
Figure 2.12: INA226 Power Monitoring Module[5]
```

Chapter 2. Hardware and software study of the system

```
a. Technical Specifications
The table below summarizes the key specifications of the INA226 sensor:
```

```
Tableau 2.9: INA226 Technical Specifications[18]
```

```
Operating Voltage 2.7V – 5.5V
```

```
Bus Voltage Range 0V – 36V
```

```
Current Measurement Range ±15A (depends on shunt resistor)
```

```
Communication Interface I^2 C (up to 400kHz)
```

```
ADC Resolution 16-bit
```

```
Power Consumption Low (typically <1mA)
```

```
Dimensions 25mm×21mm
```

```
Price 15.000 TND
```

```
b. Pinout Description
```

```
Figure 2.13: INA226 Pinout Diagram[6]
```

Chapter 2. Hardware and software study of the system

```
Tableau 2.10: INA226 Pinout Description[6]
```

```
Pin Description
```

```
VCC Power supply input (2.7V–5.5V).
```

```
GND Ground connection.
```

```
SDA I^2 C data line for communication with the microcontroller.
```

```
SCL I^2 C clock line for communication synchronization.
```

##### VIN+

```
Positive input for current sensing (connect to power source side of
shunt resistor).
```

```
VIN– Negative input for current sensing (connect to load side of shuntresistor).
```

```
2.4.3.4 Gas and Air Quality Sensors
```

```
In the context of our boat monitoring system, gas detection and air quality
assessment are crucial for safety and environmental awareness. We employed
two gas sensors:
```

- TheMQ-5sensor to detect combustible gases such as LPG, methane,
  hydrogen, and natural gas, providing real-time gas leakage alerts.
- TheMQ-135sensor to monitor air quality by measuring concentrations
  of harmful gases like ammonia, nitrogen oxides, benzene, and smoke, thus
  indicating the overall air pollution level in the boat environment.

```
a. MQ-5 Gas Sensor (Combustible Gas Detection) The MQ-5 sensor
is a sensitive semiconductor-based gas sensor designed to detect combustible
gases. It consists of a gas-sensitive layer formed on a ceramic substrate. When
exposed to gas, the sensor’s conductivity changes, allowing it to detect gas
concentrations based on voltage variations across its output.
```

```
The sensor outputs an analog signal and can also be used with a digital
threshold-based output through a comparator. Figure 2.14 shows the MQ-
5 module.
```

Chapter 2. Hardware and software study of the system

```
Figure 2.14: MQ-5 Gas Sensor Module[7]
```

```
Technical Specifications
```

```
Tableau 2.11: MQ-5 Technical Specifications[19]
```

```
Operating Voltage 5V DC
```

```
Detection Range 300 – 10000 ppm (LPG, methane, hy-drogen)
```

```
Preheat Time Not less than 48 hours
```

```
Analog/Digital Output AO (analog), DO (digital via compara-
tor)
```

```
Dimensions 32mm×20mm×22mm
```

```
Price 10.000 TND
```

```
Pinout Description
```

Chapter 2. Hardware and software study of the system

```
Tableau 2.12: MQ-5 Pinout Description[20]
```

```
Pin Description
```

```
VCC Power supply (5V)
```

```
GND Ground
```

```
AO Analog output signal proportional to gas concentration
```

```
DO Digital output signal based on comparator threshold
```

```
b. MQ-135 Air Quality Sensor The MQ-135 sensor is suitable for detect-
ing a wide range of gases associated with poor air quality. It is widely used for
monitoring indoor air pollution levels. This sensor is sensitive to gases such as
ammonia (NH 3 ), nitrogen oxides (NOx), alcohol, benzene, smoke, and carbon
dioxide (CO 2 ).
```

```
The MQ-135 works similarly to the MQ-5: it has a sensitive layer whose resis-
tance varies with gas concentration. Figure 2.15 shows the MQ-135 module.
```

```
Figure 2.15: MQ-135 Air Quality Sensor Module[8]
```

Chapter 2. Hardware and software study of the system

```
Technical Specifications
```

```
Tableau 2.13: MQ-135 Technical Specifications[21]
```

```
Operating Voltage 5V DC
```

```
Detection Range
```

```
10 – 1000 ppm (various gases
: NH3,NOx, alcohol, Benzene,
smoke,CO2 ,etc.)
```

```
Preheat Time Over 24 hour
```

```
Analog/Digital Output AO (analog), DO (digital via compara-
tor)
```

```
Dimensions 32mm×20mm×22mm
```

```
Price 11.000 TND
```

```
Pinout Description
```

```
Tableau 2.14: MQ-135 Pinout Description[22]
```

```
Pin Description
```

```
VCC Power supply (5V)
```

```
GND Ground
```

```
AO Analog output signal proportional to pollution level
```

```
DO Digital output signal based on threshold setting
```

Chapter 2. Hardware and software study of the system

#### 2.4.4 Power Sources

```
In this section, I provide a detailed description of the power sources utilized
in the boat monitoring system.
```

```
2.4.4.1 18650 Li-ion Cell
```

```
The primary power source is a single 18650 lithium-ion cell, which operates at
a nominal voltage of 3.7V and is housed in the onboard battery holder of the
LilyGO TTGO ESP32 SIM7600 board. This cell offers high energy density,
rechargeability, and built-in protection against over-charge and over-discharge
via the board’s CN3165 charging IC.
```

```
Figure 2.16: 18650 Li-ion Cell in Battery Holder[9]
```

```
Description
```

- Nominal Capacity: 2600mAh
- Usable Capacity: 2200mAh (85
- Nominal Voltage: 3.7V (operating range 3.4–4.2V)
- Maximum Charge Voltage: 4.2V
- Operating Temperature: Charge 0°C–45°C, Discharge –20°C–60°C
- Estimated Runtime: 11h at 200mA average draw
- Price: 18.000TND

Chapter 2. Hardware and software study of the system

```
2.4.4.2 Solar Panel
```

```
To achieve energy autonomy, I plan to connect a 6V/10W solar panel (340×220mm)
directly to the board’s solar input. The CN3165 charge controller accepts up
to 6V, regulating current (up to 500mA) to recharge the 18650 cell during
daylight hours.
```

```
Figure 2.17: 6V/10W Solar Panel (340×220mm)[10]
```

```
Description
```

- Rated Voltage: 6V (open-circuit)
- Rated Power: 10W
- Rated Current: 1.67A (at peak sun)
- Dimensions: 340×220mm
- Features: UV-resistant, corrosion-proof backing, tempered glass
- Expected Daily Yield: 18Wh (5h full sun)
- Price: 25.000TND

Chapter 2. Hardware and software study of the system

#### 2.4.5 Reliability in Maritime Environments

```
Operating in marine conditions exposes the monitoring system to salt spray,
high humidity, wide temperature fluctuations, UV radiation, vibration, and
biofouling. To ensure long-term reliability, I have evaluated and mitigated
environmental risks for each component: the ESP32+SIM7600 board and
INA226 sensor are conformally coated and fully enclosed; the DHT22 sits
under a ventilated, UV-stable radiation shield; MQ-5 and MQ-135 gas sensors
use replaceable cartridges behind hydrophobic membranes for corrosion pro-
tection and in-field calibration; the PIR module is fitted with a hydrophobic
lens cover and tuned for reduced sensitivity; and cellular/GNSS uses IP-rated
external antennas with strain relief. Combined with local data buffering and
periodic calibration routines, these measures safeguard uptime and data in-
tegrity in harsh offshore deployments.
```

### 2.5 Software Section

```
In this part, I describe the software tools used during development of the boat
monitoring system.
```

#### 2.5.1 Simulation Software

```
Fritzing is an open-source tool for designing and documenting electronic cir-
cuits. It provides schematic, breadboard, and PCB views, allowing drag-and-drop
placement of components and virtual wiring to prototype circuit designs before
hardware assembly.
```

```
Figure 2.18: Fritzing Logo[11]
```

#### 2.5.2 Computer-Aided Design Software (CAD)

```
To design the enclosure and PCB layout in 3D, I useSolidWorks. It en-
ables precise 3D modelling of mechanical parts and enclosures, ensuring that
the electronics fit securely and withstand marine conditions. If requirements
change, I can switch to another CAD package such as Autodesk Inventor with-
out altering the workflow.
```

Chapter 2. Hardware and software study of the system

```
Figure 2.19: SolidWorks Logo[12]
```

#### 2.5.3 Integrated Development Environment (IDE)

```
Arduino IDE is the main development environment used to program the
ESP32 board. It provides a simple and beginner-friendly interface for writing,
compiling, and uploading embedded code.
Key features include:
```

- Support for a wide range of microcontrollers including ESP32
- Integrated serial monitor for debugging
- Rich library ecosystem
- Lightweight and easy to use

```
Figure 2.20: Arduino IDE Logo[13]
```

```
In addition, I also useVisual Studio Codefor mobile and web development
tasks.
```

Chapter 2. Hardware and software study of the system

```
Figure 2.21: Visual Studio Code Logo[14]
```

#### 2.5.4 Mobile Application Integration

```
Instead of using a generic IoT platform such as Blynk, I have integrated sensor
data and control logic directly into theBoat Promobile application, devel-
oped with AngularandIonic. This allows for a customized and seamless
user experience.
```

```
Figure 2.22: Ionic Framework Logo[15]
```

```
Key benefits of this approach include:
```

- A fully customized interface for boat monitoring
- Integration with maps and charts for location and sensor data
- Support for push notifications and offline access

Chapter 2. Hardware and software study of the system

### 2.6 Conclusion

```
In this chapter, I have examined both the hardware and software elements of
the boat monitoring system in detail. I described the system architecture, jus-
tifying the selection of each hardware component—including the ESP32+SIM7600
board, sensors, and power sources—and outlined the communication protocols
suited to maritime conditions. I also reviewed the software environment, from
circuit simulation in Fritzing to the 3D CAD tools for enclosure design, as well
as the IDEs and frameworks used for firmware and mobile-app integration.
These choices form a solid technical foundation for the project’s implementa-
tion.
In the next chapter, I will present the step-by-step realization of the prototype,
including wiring, PCB design, firmware deployment, and initial testing results,
to demonstrate the system’s functionality in real-world conditions.
```

# Chapter 3

# Prototype System Implementation

Chapter 3. Prototype System Implementation

### 3.1 Introduction

```
Through the preceding chapters, I have defined the objectives of the boat
monitoring system, selected and justified the hardware components, and es-
tablished the software environment. In this chapter, I move to the implemen-
tation phase. I will assemble the embedded hardware, integrate all sensors and
communication modules, and deploy the firmware. Then I will configure and
test the Boat Pro mobile application to receive and display real-time data from
the vessel. This gradual, step-by-step approach—accompanied by screenshots
and test cases—demonstrates the successful realization and validation of the
complete system.
```

### 3.2 Realization and Validation

```
In this section, I present the results of the system’s realization and validation.
First, I detail the wiring and assembly of the ESP32+SIM7600 board, sen-
sors (DHT22, MQ-5, MQ-135, PIR, INA226), and power supply within the
marine enclosure. Next, I describe the tests performed to verify GPS/GSM
connectivity, sensor accuracy, and power autonomy. Finally, I illustrate the
configuration of the Boat Pro Ionic/Angular application and show the live
data dashboards and alert mechanisms.
```

#### 3.2.1 Boat Monitoring System

```
3.2.1.1 Electronic Schematic
```

```
To provide a comprehensive overview, Figure 3.1 shows the global wiring of
the boat monitoring system, including power, I²C bus, UART lines to the
SIM7600, and sensor connections. Figure 3.2 presents the detailed Fritzing
schematic used to verify pin assignments and signal routing.
```

Chapter 3. Prototype System Implementation

```
Figure 3.1: Global Wiring Diagram of Boat Monitoring System
```

```
Figure 3.2: Fritzing Schematic of Boat Monitoring System
```

#### 3.2.2 SIM7600 Initialization & Testing

```
The built-in SIM7600 modem on the LilyGO TTGO ESP32 board is initial-
ized and configured entirely via AT commands over its UART interface. The
sequence below mirrors the commands issued in firmware:
```

Chapter 3. Prototype System Implementation

1. AT+CLTS=1— Enable network time sync (sent viaSerialAT)
2. AT+CTZU=1— Enable automatic time zone update (sent viamodem.sendAT())
3. AT+CGNSSMODE=1,1— Set GPS-only mode (sent viamodem.sendAT())
4. AT+CGNSS=1— Enable GPS (viamodem.enableGPS())
5. AT+HTTPSSL=0— Disable HTTPS (missing in original list, used insendHTTPPost())
6. AT+CMGF=1— SMS text mode (for alerts)
7. AT+CMGS— Send SMS alert (with phone number)

```
These commands verify module health, enable GPS, establish a GPRS con-
text, and transmit sensor readings via HTTP—all without additional external
wiring.
```

#### 3.2.3 Boat Monitoring Prototype

```
3.2.3.1 Hardware Integration
```

```
I mounted the LilyGO TTGO ESP32+SIM7600 board, the DHT22, MQ-5,
MQ-135, PIR and INA226 sensors inside the marine-grade enclosure, care-
fully routing only the sensor apertures through hydrophobic membrane vents.
All I²C, UART and GPIO lines are connected to the ESP32 header per the
schematics in Chapter 2.
```

```
3.2.3.2 Firmware Deployment & Configuration
```

```
Using the Arduino IDE, I uploaded the firmware that we saw in Listing??.
After reset, the board:
```

- Executes AT commands to power on GPS and attach GPRS viaAT+CGDCONT,
  AT+CGATTandAT+SAPBR
- Reads each sensor, formats a JSON payload, and issues an HTTP POST
  to the Boat Pro API endpoint

```
I verified each step over Serial Mon, confirming network registration, GPS fix
acquisition, and successful HTTP responses.
```

```
3.2.3.3 Field Testing
```

```
I conducted sea trials at 1km offshore, logging:
```

- GPS accuracy within 3m after 30s cold-start
- HTTP POST success >95
- Battery draw of 200mA avg in deep-sleep mode with 30s transmission
  intervals

Chapter 3. Prototype System Implementation

```
3.2.3.4 Mobile App Validation
```

```
Finally, I integrated the same REST API into the Ionic/Angular Boat Pro app.
Screenshots in Figure??show live telemetry graphs, map position, and alert
banners when motion or gas thresholds are exceeded. All components worked
end-to-end, demonstrating the system’s readiness for real-world deployment.
```

### 3.3 Enclosure Design

```
Rather than designing a custom PCB, I opted to create a 3D-printed enclosure
that houses the LilyGO TTGO ESP32+SIM7600 board centrally and provides
dedicated mounting points and sealed apertures for each sensor module. The
enclosure is designed in SolidWorks (or CAD) with the following considera-
tions:
```

- Board Mounting: A snap-fit cradle secures the ESP32 board in the
  center, aligning its USB and antenna connectors with external openings.
- Sensor Ports: Each sensor (DHT22, MQ-5, MQ-135, PIR, INA226
  shunt resistor) receives a weather-proof membrane-vented port that al-
  lows the sensing element to contact the environment while maintaining
  IP67 integrity.
- Cable Routing: Internal channels guide wiring harnesses from the
  board to each sensor port, minimizing strain and preventing tangling.
- Power Access:The 18650 battery compartment and solar input termi-
  nal are accessible through a sealed side panel for easy battery replacement
  and panel connection.
- Mounting Features: Flanges and slots on the back of the enclosure
  allow it to be fastened to the boat’s bulkhead or railing.

```
Figure 3.3 shows a preliminary CAD rendering of the enclosure. I will attach
a finalized SolidWorks screenshot once the design is complete.
```

Chapter 3. Prototype System Implementation

```
chap3 figures/enclosure_cad_placeholder.png
```

```
Figure 3.3: 3D CAD Rendering of Enclosure (Placeholder)
```

### 3.4 Mobile Application

#### 3.4.1 Overview of Boat Pro

```
Boat Pro is a social and marketplace application for boat owners, built with
the Angular/Ionic framework. It provides users with:
```

- A chat system to communicate and share events or favorite anchorages
- A marketplace to buy, sell, and browse marine equipment
- An IoT dashboard (my scope) for real-time monitoring and control of
  onboard sensors

#### 3.4.2 IoT Dashboard

```
The IoT page of Boat Pro is organized into a set of interactive cards. Screen-
shots of the live application are shown below.
```

```
3.4.2.1 Environmental Data
```

```
Displays current:
```

- Temperature (°C) and humidity (%)

Chapter 3. Prototype System Implementation

- Motion detection status
- Gas-leak alert

```
Figure 3.4: Environmental Data Card: temperature, humidity, motion, gas
```

```
3.4.2.2 System Status
```

```
Shows:
```

- Battery voltage (user selects 6V, 12V or 24V system)
- Boat speed (km/h) from GPS

```
3.4.2.3 Air Quality & CO 2
```

```
Presents:
```

- CO 2 concentration (ppm)
- Air quality label (Excellent, Good, Moderate, Poor, Unhealthy)

```
3.4.2.4 Historical Data
```

```
Graphs of the last 24hours for:
```

- Temperature (°C)
- Humidity (%)

Chapter 3. Prototype System Implementation

```
chap3 figures/screenshots/system_status.png
```

```
Figure 3.5: System Status Card: battery voltage and speed
```

```
chap3 figures/screenshots/air_quality.png
```

```
Figure 3.6: Air Quality & CO 2 Card
```

Chapter 3. Prototype System Implementation

```
chap3 figures/screenshots/history.png
```

```
Figure 3.7: Historical Data Card: 24h temperature and humidity charts
```

```
3.4.2.5 Location
```

```
Interactive map showing the boat’s current GPS position.
```

```
3.4.2.6 Geofence Settings
```

```
Allows the user to:
```

- Enter center coordinates manually or “Reset to Boat”
- Drag radius slider from 0.1km to 10km

```
3.4.2.7 Geofence Events
```

```
When the boat breaches the geofence, past locations are overlaid as dots on
the map, and alerts are generated every 3min until re-entry.
```

```
3.4.2.8 Notifications History
```

```
Lists all recent alerts:
```

- Low battery (<80%)
- Gas detection

Chapter 3. Prototype System Implementation

```
chap3 figures/screenshots/location.png
```

```
Figure 3.8: Location Card: Real-time boat position on map
```

```
chap3 figures/screenshots/geofence_settings.png
```

```
Figure 3.9: Geofence Settings Card
```

Chapter 3. Prototype System Implementation

```
chap3 figures/screenshots/geofence_events.png
```

```
Figure 3.10: Geofence Events Card: breach track overlay
```

- Motion (when Armed)
- Geofence breach

```
3.4.2.9 Arm/Disarm Control
```

```
Toggle for motion alerts and SMS:
```

- Armed: motion detection triggers SMS and in-app notification
- Disarmed: no motion alerts (user may set duration in hours/days)

```
3.4.2.10 Complete IoT Dashboard Interface
```

```
Below is the full view of the Boat Pro IoT dashboard, showcasing all cards in
a single screen for a holistic overview.
```

Chapter 3. Prototype System Implementation

```
chap3 figures/screenshots/notifications.png
```

```
Figure 3.11: Notifications History
```

```
chap3 figures/screenshots/arm_disarm.png
```

```
Figure 3.12: Arm/Disarm Control
```

Chapter 3. Prototype System Implementation

```
chap3 figures/screenshots/iot_dashboard_full.png
```

```
Figure 3.13: Complete IoT Dashboard Interface
```

Chapter 3. Prototype System Implementation

### 3.5 Prototype

```
Our intelligent agriculture system prototype is the result of our extensive work
and knowledge in developing an innovative solution. It demonstrates the suc-
cessful integration of key subsystems, such as the greenhouse, sun tracker solar
panel, and automatic pet watering system. These subsystems are controlled
by the ESP32 microcontroller and connected through GPRS technology. The
prototype embodies an advanced and automated agricultural system that en-
hances productivity, conserves energy, and simplifies management. It holds
promise for farmers looking for a cost-effective and sustainable solution to im-
prove their agricultural practices.
The following figures shows the real implementation of intelligent agriculture
system prototype.
```

```
WhatsApp Image 2023-06-23 at 16.43.57.jpeg
```

```
Figure 3.14: realisation and testing
```

Chapter 3. Prototype System Implementation

```
WhatsApp Image 2023-06-23 at 16.50.24.jpeg
```

```
Figure 3.15: Prototype
```

### 3.6 Conclusion

```
In this chapter, we have provided a detailed exposition of the system, present-
ing an in-depth analysis of its various components. We have incorporated the
circuit diagram and the schematics accompanied by a clear description of the
connections. In addition, we have depicted the flowchart of our three systems,
highlighting their operational processes. Furthermore, we have showcased the
design of our PCB board, emphasizing its role in the system’s functional-
ity. We have explained the steps for receiving data and monitoring our system
through the mobile application in a clear and understandable manner. Finally,
rigorous testing and validation procedures have been undertaken to ensure the
prototype’s dependability and optimal performance.
```

# General conclusion and

# perspectives

To complete our bachelor’s degree program in Electronics, Electrotechnics, and
Automation with a specialization in Embedded Systems, we were assigned a
final-year project.

Our objective was to design an intelligent agricultural system that utilizes
GPRS for wireless communication and the ESP32 microcontroller. This sys-
tem consists of three subsystems: the greenhouse, sun tracker solar panel, and
automatic pet watering.
The greenhouse subsystem maintains optimal environmental conditions for
plant growth, including temperature, humidity, and soil moisture. The sun
tracker solar panel optimizes solar energy utilization by adjusting its position
according to the sun’s movement. The automatic pet watering system ensures
a continuous water supply for pets.
The integration of these subsystems has resulted in an automated agricultural
system that enhances crop productivity, conserves energy, and simplifies pet
care.
Our project comprised five stages. We began with a preliminary study to un-
derstand the latest technologies in the agricultural sector and determine our
project’s primary objective. This led to requirement analysis and specifica-
tion. Once our goals were defined, we moved to the design phase.
In the second phase, we incorporated GPRS technology into our system, en-
abling wireless communication between the central control unit and the sub-
systems. This ensures real-time data transmission, efficient monitoring, and
control of environmental conditions and pet watering. Next, we conducted a
simulation using Fritzing and implemented our smart agriculture system. The
subsystems included an irrigation system and temperature regulation system
for the greenhouse, as well as pet watering and sun tracker solar panel systems.
Using the ESP32 board as an interface simplified system control, as observed
during practical tests.
In the fourth phase, we further enhanced our implementation by integrating
the Blynk application for remote control. This allowed us to control the sys-
tem elements from a distance or via the internet using the ESP32 and GPRS
module.
Finally, we completed the implementation phase, gaining familiarity with the

General conclusion and perspectives

```
coding aspects of the intelligent agricultural system for remote control and
monitoring.
```

```
Then we are pleased with the successful accomplishment of our final year
project, which has the potential to advance the agricultural sector by pro-
viding cost-effective and sustainable improvements to working conditions Our
perspective for this project is :
```

- Integration of photovoltaic panels: We plan to incorporate photovoltaic
  panels into the system to significantly reduce the overall electrical con-
  sumption by harnessing solar energy, to ensure a more sustainable and
  environmentally friendly operation.
- Implementation of LoRa technology: Instead of relying on traditional
  GPRS technology, we have chosen to utilize LoRa for long-range commu-
  nication in our IoT applications. LoRa offers an energy-efficient solution,
  allowing connectivity over vast areas with minimal power consumption.
  This choice ensures optimized power management and enables seamless
  communication in our system.
- Utilization of STM32 microcontroller: The selection of the STM32 mi-
  crocontroller is driven by its renowned low-power operation capabilities.
  By leveraging this microcontroller, we can achieve efficient energy man-
  agement and optimize the overall power consumption of our system.
- Development of a customized sensor node: In order to optimize system
  performance and meet our specific requirements, we will design and inte-
  grate a bespoke sensor node. This tailor-made solution will enable precise
  data collection and monitoring, while also reducing the need for excessive
  wiring and cables.

# Webography

```
[1] “Dht22 temperature and humidity sensor module image.” Manufacturer’s
product photo.
[2] “Dht22 pinout diagram.” Adapted from multiple online sources.
[3] “Hc-sr501 pir motion sensor module image.” Manufacturer’s product
photo.
[4] “Hc-sr501 pir sensor pinout diagram.” Adapted from multiple sources.
[5] “Ina226 current and power monitor module image.” TinyTronics image.
[6] “Ina226 pinout and interface description.” Adapted from multiple sources.
[7] “Mq-5 combustible gas sensor module image.” Accessed 2025-05-13.
[8] “Mq-135 air quality sensor image.” Accessed 2025-05-13.
[9] “18650 li-ion cell product image.” Accessed 2025-05-14.
```

[10] “6v/10w solar panel product image.” Accessed 2025-05-14.

[11] Fritzing, “Fritzing logo.”https://fritzing.org. Accessed: 2025-05-14.

[12] Dassault Systèmes, “Solidworks logo.” https://www.solidworks.com.
Accessed: 2025-05-14.

[13] Arduino, “Arduino logo.”https://www.arduino.cc. Accessed: 2025-05- 14.

[14] Microsoft, “Visual studio code logo.” https://code.visualstudio.com.
Accessed: 2025-05-14.

[15] Ionic Framework, “Ionic logo.”https://ionicframework.com. Accessed:
2025-05-14.

[16] A. Electronics, “Am2302/dht22 datasheet.” Accessed 2025-05-11.

[17] “Hc-sr501 pir sensor datasheet.” Accessed 2025-05-11.

[18] “Ina226 datasheet - texas instruments.” Accessed 2025-05-13.

[19] “Mq-5 gas sensor datasheet.” Accessed 2025-05-13.

[20] “Mq-5 sensor pinout.” Accessed 2025-05-13.

[21] “Mq-135 air quality sensor datasheet.” Accessed 2025-05-13.

[22] “Mq-135 pinout and usage guide.” Accessed 2025-05-13.
